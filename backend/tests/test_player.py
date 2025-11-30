"""
Tests for player endpoints.
"""
import pytest


def test_get_player_profile_success(client, auth_headers):
    """Test getting player profile."""
    response = client.get("/api/player/profile", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "username" in data
    assert data["username"] == "testuser"
    assert "score" in data
    assert "highScore" in data
    assert "gamesPlayed" in data
    assert data["score"] >= 0
    assert data["highScore"] >= 0
    assert data["gamesPlayed"] >= 0


def test_get_player_profile_unauthorized(client):
    """Test getting player profile without authentication."""
    response = client.get("/api/player/profile")
    
    assert response.status_code == 401


def test_get_player_profile_invalid_token(client):
    """Test getting player profile with invalid token."""
    response = client.get(
        "/api/player/profile",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    
    assert response.status_code == 401


def test_player_profile_after_score_submission(client, auth_headers):
    """Test that player profile updates after score submission."""
    # Get initial profile
    response = client.get("/api/player/profile", headers=auth_headers)
    initial_profile = response.json()
    initial_games = initial_profile["gamesPlayed"]
    initial_high_score = initial_profile["highScore"]
    
    # Submit a high score
    client.post(
        "/api/game/score",
        json={"score": 500, "mode": "walls"},
        headers=auth_headers
    )
    
    # Get updated profile
    response = client.get("/api/player/profile", headers=auth_headers)
    updated_profile = response.json()
    
    # Verify updates
    assert updated_profile["gamesPlayed"] == initial_games + 1
    assert updated_profile["highScore"] >= initial_high_score
