import pytest


class TestUnregister:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_success(self, client, sample_email, sample_activity):
        """Arrange-Act-Assert: Successfully unregister from an activity."""
        # Arrange
        from app import activities
        activities[sample_activity]["participants"].append(sample_email)
        initial_count = len(activities[sample_activity]["participants"])

        # Act
        response = client.delete(
            f"/activities/{sample_activity}/unregister",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert sample_email not in activities[sample_activity]["participants"]
        assert len(activities[sample_activity]["participants"]) == initial_count - 1

    def test_unregister_activity_not_found(self, client, sample_email):
        """Test unregister fails when activity doesn't exist."""
        # Arrange
        fake_activity = "Nonexistent Activity"

        # Act
        response = client.delete(
            f"/activities/{fake_activity}/unregister",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_student_not_signed_up(self, client, sample_email, sample_activity):
        """Test unregister fails when student is not signed up."""
        # Arrange
        # (student not added to participants)

        # Act
        response = client.delete(
            f"/activities/{sample_activity}/unregister",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_one_participant_among_many(self, client, sample_email, sample_activity):
        """Test unregistering one participant doesn't affect others."""
        # Arrange
        from app import activities
        other_emails = ["user1@mergington.edu", "user2@mergington.edu", "user3@mergington.edu"]
        for email in other_emails + [sample_email]:
            activities[sample_activity]["participants"].append(email)

        # Act
        response = client.delete(
            f"/activities/{sample_activity}/unregister",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 200
        assert sample_email not in activities[sample_activity]["participants"]
        for email in other_emails:
            assert email in activities[sample_activity]["participants"]
        assert len(activities[sample_activity]["participants"]) == 3

    def test_unregister_response_format(self, client, sample_email, sample_activity):
        """Test that unregister response has correct format."""
        # Arrange
        from app import activities
        activities[sample_activity]["participants"].append(sample_email)

        # Act
        response = client.delete(
            f"/activities/{sample_activity}/unregister",
            params={"email": sample_email}
        )
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert sample_email in data["message"]
        assert sample_activity in data["message"]
