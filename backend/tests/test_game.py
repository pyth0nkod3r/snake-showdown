"""
Tests for game endpoints.
"""


def test_submit_score_success(client, auth_headers):
    """Test successful score submission."""
    response = client.post(
        "/api/game/score",
        json={"score": 150, "mode": "walls"},
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Score submitted successfully"
    assert "isNewHighScore" in data
    assert "rank" in data


def test_submit_score_unauthorized(client):
    """Test score submission without authentication."""
    response = client.post(
        "/api/game/score",
        json={"score": 150, "mode": "walls"}
    )
    
    assert response.status_code == 401


def test_submit_score_negative(client, auth_headers):
    """Test submitting negative score."""
    response = client.post(
        "/api/game/score",
        json={"score": -10, "mode": "walls"},
        headers=auth_headers
    )
    
    assert response.status_code == 422


def test_submit_score_invalid_mode(client, auth_headers):
    """Test submitting score with invalid mode."""
    response = client.post(
        "/api/game/score",
        json={"score": 150, "mode": "invalid"},
        headers=auth_headers
    )
    
    assert response.status_code == 422


def test_get_leaderboard_success(client):
    """Test getting leaderboard."""
    response = client.get("/api/game/leaderboard")
    
    assert response.status_code == 200
    data = response.json()
    assert "entries" in data
    assert "total" in data
    assert isinstance(data["entries"], list)


def test_get_leaderboard_with_mode_filter(client):
    """Test getting leaderboard filtered by mode."""
    response = client.get("/api/game/leaderboard?mode=walls")
    
    assert response.status_code == 200
    data = response.json()
    assert "entries" in data


def test_get_leaderboard_with_pagination(client):
    """Test leaderboard pagination."""
    response = client.get("/api/game/leaderboard?limit=3&offset=0")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["entries"]) <= 3


def test_get_leaderboard_invalid_limit(client):
    """Test leaderboard with invalid limit."""
    response = client.get("/api/game/leaderboard?limit=200")
    
    assert response.status_code == 422


def test_get_live_games_success(client):
    """Test getting live games."""
    response = client.get("/api/game/live")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    if len(data) > 0:
        game = data[0]
        assert "id" in game
        assert "player" in game
        assert "gameState" in game
        assert "startedAt" in game


def test_get_live_games_with_mode_filter(client):
    """Test getting live games filtered by mode."""
    response = client.get("/api/game/live?mode=passthrough")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_live_games_with_limit(client):
    """Test live games with limit."""
    response = client.get("/api/game/live?limit=2")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 2


def test_leaderboard_entry_structure(client):
    """Test leaderboard entry has correct structure."""
    response = client.get("/api/game/leaderboard?limit=1")
    
    assert response.status_code == 200
    data = response.json()
    
    if len(data["entries"]) > 0:
        entry = data["entries"][0]
        assert "rank" in entry
        assert "username" in entry
        assert "score" in entry
        assert "date" in entry
        assert entry["rank"] >= 1
        assert entry["score"] >= 0


def test_live_game_structure(client):
    """Test live game has correct structure."""
    response = client.get("/api/game/live?limit=1")
    
    assert response.status_code == 200
    data = response.json()
    
    if len(data) > 0:
        game = data[0]
        assert "player" in game
        assert "gameState" in game
        
        # Check game state structure
        state = game["gameState"]
        assert "snake" in state
        assert "food" in state
        assert "score" in state
        assert "isGameOver" in state
        assert "isPaused" in state
        assert "mode" in state
        
        # Check snake structure
        snake = state["snake"]
        assert "body" in snake
        assert "direction" in snake
        assert len(snake["body"]) > 0
