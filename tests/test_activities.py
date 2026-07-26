import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_success(self, client):
        """Arrange-Act-Assert: Get all activities successfully."""
        # Arrange
        expected_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0
        
        # Verify each activity has required fields
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert all(field in activity_data for field in expected_fields)

    def test_get_activities_structure(self, client, populated_activities):
        """Test that activities contain expected data structure."""
        # Arrange
        # (populated_activities fixture sets up data)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        
        # Check specific activity
        chess_club = activities.get("Chess Club")
        assert chess_club is not None
        assert "description" in chess_club
        assert isinstance(chess_club["description"], str)
        assert isinstance(chess_club["participants"], list)
        assert len(chess_club["participants"]) == 2

    def test_get_activities_participants_visible(self, client, sample_email, sample_activity):
        """Test that participants are visible in activities list."""
        # Arrange
        from app import activities
        activities[sample_activity]["participants"].append(sample_email)

        # Act
        response = client.get("/activities")
        activity_data = response.json()[sample_activity]

        # Assert
        assert response.status_code == 200
        assert sample_email in activity_data["participants"]

    def test_get_activities_availability(self, client, sample_activity):
        """Test that max_participants and participants are correct."""
        # Arrange
        from app import activities
        activity = activities[sample_activity]
        initial_count = len(activity["participants"])
        max_participants = activity["max_participants"]

        # Act
        response = client.get("/activities")
        activity_response = response.json()[sample_activity]

        # Assert
        assert response.status_code == 200
        assert activity_response["max_participants"] == max_participants
        assert len(activity_response["participants"]) == initial_count
