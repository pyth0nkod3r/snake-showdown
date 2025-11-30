"""
Test fixtures and configuration.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import db


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    """Create authenticated user and return auth headers."""
    # Create a test user
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "test@example.com",
            "password": "testpass123",
            "username": "testuser"
        }
    )
    assert response.status_code == 201
    
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each test."""
    # Store original state
    original_users = db.users.copy()
    original_players = db.players.copy()
    original_scores = db.scores.copy()
    
    yield
    
    # Restore original state
    db.users = original_users
    db.players = original_players
    db.scores = original_scores
