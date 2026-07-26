import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add src to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Create a FastAPI test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to a known state before each test."""
    # Clear all participants to start fresh
    for activity in activities.values():
        activity["participants"] = []
    yield
    # Clean up after test
    for activity in activities.values():
        activity["participants"] = []


@pytest.fixture
def sample_email():
    """Generate a sample email for testing."""
    import random
    import string
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_id}@mergington.edu"


@pytest.fixture
def sample_activity():
    """Get the first activity name for testing."""
    return list(activities.keys())[0]


@pytest.fixture
def populated_activities():
    """Populate activities with sample participants."""
    activities["Chess Club"]["participants"] = ["alice@mergington.edu", "bob@mergington.edu"]
    activities["Programming Class"]["participants"] = ["charlie@mergington.edu"]
    yield activities
    # Reset after test
    for activity in activities.values():
        activity["participants"] = []
