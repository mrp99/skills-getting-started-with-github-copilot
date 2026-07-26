import pytest


class TestSignup:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client, sample_email, sample_activity):
        """Arrange-Act-Assert: Successfully sign up for an activity."""
        # Arrange
        from app import activities
        initial_count = len(activities[sample_activity]["participants"])

        # Act
        response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]
        assert sample_email in activities[sample_activity]["participants"]
        assert len(activities[sample_activity]["participants"]) == initial_count + 1

    def test_signup_activity_not_found(self, client, sample_email):
        """Test signup fails when activity doesn't exist."""
        # Arrange
        fake_activity = "Nonexistent Activity"

        # Act
        response = client.post(
            f"/activities/{fake_activity}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_student(self, client, sample_email, sample_activity):
        """Test signup fails when student is already registered."""
        # Arrange
        from app import activities
        activities[sample_activity]["participants"].append(sample_email)

        # Act
        response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_multiple_activities(self, client, sample_email):
        """Test that student can sign up for multiple activities."""
        # Arrange
        from app import activities
        activities_list = list(activities.keys())[:2]
        
        # Act
        response1 = client.post(
            f"/activities/{activities_list[0]}/signup",
            params={"email": sample_email}
        )
        response2 = client.post(
            f"/activities/{activities_list[1]}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert sample_email in activities[activities_list[0]]["participants"]
        assert sample_email in activities[activities_list[1]]["participants"]

    def test_signup_response_message_format(self, client, sample_email, sample_activity):
        """Test that signup response has correct message format."""
        # Arrange
        # (no special setup needed)

        # Act
        response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email}
        )
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert "message" in data
        assert "Signed up" in data["message"]
        assert sample_email in data["message"]
        assert sample_activity in data["message"]

    def test_signup_different_emails(self, client, sample_activity):
        """Test multiple different emails can sign up for same activity."""
        # Arrange
        from app import activities
        emails = [f"user{i}@mergington.edu" for i in range(3)]

        # Act & Assert
        for email in emails:
            response = client.post(
                f"/activities/{sample_activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
            assert email in activities[sample_activity]["participants"]
