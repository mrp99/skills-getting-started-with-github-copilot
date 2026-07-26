import pytest


class TestIntegration:
    """Integration tests for complete activity signup/unregister flows."""

    def test_complete_signup_view_unregister_flow(self, client, sample_email, sample_activity):
        """Test complete flow: signup -> view participants -> unregister."""
        # Arrange
        from app import activities

        # Act - Step 1: Sign up
        signup_response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email}
        )

        # Assert - Step 1
        assert signup_response.status_code == 200
        assert sample_email in activities[sample_activity]["participants"]

        # Act - Step 2: Get activities and verify participant is visible
        get_response = client.get("/activities")
        activity_data = get_response.json()[sample_activity]

        # Assert - Step 2
        assert get_response.status_code == 200
        assert sample_email in activity_data["participants"]

        # Act - Step 3: Unregister
        unregister_response = client.delete(
            f"/activities/{sample_activity}/unregister",
            params={"email": sample_email}
        )

        # Assert - Step 3
        assert unregister_response.status_code == 200
        assert sample_email not in activities[sample_activity]["participants"]

        # Act - Step 4: Verify participant is no longer visible
        final_response = client.get("/activities")
        final_activity_data = final_response.json()[sample_activity]

        # Assert - Step 4
        assert final_response.status_code == 200
        assert sample_email not in final_activity_data["participants"]

    def test_multiple_signups_same_activity(self, client, sample_activity):
        """Test multiple students signing up for the same activity."""
        # Arrange
        from app import activities
        emails = [f"student{i}@mergington.edu" for i in range(5)]

        # Act
        for email in emails:
            response = client.post(
                f"/activities/{sample_activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Assert
        get_response = client.get("/activities")
        activity_data = get_response.json()[sample_activity]
        for email in emails:
            assert email in activity_data["participants"]
        assert len(activity_data["participants"]) == 5

    def test_student_signup_multiple_activities(self, client, sample_email):
        """Test one student signing up for multiple activities."""
        # Arrange
        from app import activities
        activities_list = list(activities.keys())[:3]

        # Act
        for activity in activities_list:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": sample_email}
            )
            assert response.status_code == 200

        # Assert
        get_response = client.get("/activities")
        activities_data = get_response.json()
        for activity in activities_list:
            assert sample_email in activities_data[activity]["participants"]

    def test_signup_unregister_signup_again(self, client, sample_email, sample_activity):
        """Test that student can unregister and sign up again."""
        # Arrange
        # (no special setup)

        # Act - First signup
        response1 = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email}
        )
        assert response1.status_code == 200

        # Act - Unregister
        response2 = client.delete(
            f"/activities/{sample_activity}/unregister",
            params={"email": sample_email}
        )
        assert response2.status_code == 200

        # Act - Sign up again
        response3 = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response3.status_code == 200
        from app import activities
        assert sample_email in activities[sample_activity]["participants"]
