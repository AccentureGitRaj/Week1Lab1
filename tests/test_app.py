import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities

def test_get_activities():
    # Arrange: nothing to set up
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Test successful signup

def test_signup_success():
    # Arrange
    email = "testuser1@mergington.edu"
    activity = "Art Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Cleanup
    client.post(f"/activities/{activity}/unregister?email={email}")

# Test duplicate signup

def test_signup_duplicate():
    # Arrange
    email = "testuser2@mergington.edu"
    activity = "Drama Society"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    client.post(f"/activities/{activity}/unregister?email={email}")

# Test signup for non-existent activity

def test_signup_nonexistent_activity():
    # Arrange
    email = "testuser3@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

# Test unregister participant

def test_unregister_success():
    # Arrange
    email = "testuser4@mergington.edu"
    activity = "Math Olympiad"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]

# Test unregister non-existent participant

def test_unregister_nonexistent_participant():
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Science Club"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
