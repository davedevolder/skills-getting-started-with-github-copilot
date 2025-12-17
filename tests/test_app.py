import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success():
    # First, get initial participants
    response = client.get("/activities")
    initial_data = response.json()
    initial_count = len(initial_data["Chess Club"]["participants"])
    
    # Signup
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    assert "Signed up test@example.com for Chess Club" in response.json()["message"]
    
    # Check updated
    response = client.get("/activities")
    data = response.json()
    assert len(data["Chess Club"]["participants"]) == initial_count + 1
    assert "test@example.com" in data["Chess Club"]["participants"]

def test_signup_duplicate():
    # Signup again
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/Invalid%20Activity/signup?email=test@example.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_success():
    # Unregister
    response = client.delete("/activities/Chess%20Club/unregister?email=test@example.com")
    assert response.status_code == 200
    assert "Unregistered test@example.com from Chess Club" in response.json()["message"]
    
    # Check removed
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" not in data["Chess Club"]["participants"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess%20Club/unregister?email=notsigned@example.com")
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]

def test_unregister_invalid_activity():
    response = client.delete("/activities/Invalid%20Activity/unregister?email=test@example.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]