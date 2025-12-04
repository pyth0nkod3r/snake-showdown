"""
Integration tests for API endpoints.
Tests complete API workflows end-to-end with real database.
"""


def test_complete_auth_flow(integration_client):
    """Test complete authentication flow: signup -> login -> get user info."""
    # Signup
    signup_response = integration_client.post(
        "/api/auth/signup",
        json={
            "email": "fullflow@example.com",
            "username": "fullflowuser",
            "password": "securepass123",
        },
    )

    assert signup_response.status_code == 201
    signup_data = signup_response.json()
    assert "user" in signup_data
    assert "token" in signup_data
    assert signup_data["user"]["email"] == "fullflow@example.com"

    signup_token = signup_data["token"]

    # Login
    login_response = integration_client.post(
        "/api/auth/login",
        json={"email": "fullflow@example.com", "password": "securepass123"},
    )

    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "token" in login_data

    # Get user info using token
    user_response = integration_client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {signup_token}"}
    )

    assert user_response.status_code == 200
    user_data = user_response.json()
    assert user_data["email"] == "fullflow@example.com"
    assert user_data["username"] == "fullflowuser"


def test_complete_game_flow(integration_client, auth_headers_integration):
    """Test complete game flow: submit scores -> check leaderboard -> verify rankings."""
    # Submit first score
    score1_response = integration_client.post(
        "/api/game/score",
        json={"score": 100, "mode": "walls"},
        headers=auth_headers_integration,
    )

    assert score1_response.status_code == 201
    score1_data = score1_response.json()
    assert score1_data["isNewHighScore"] is True
    assert score1_data["rank"] >= 1

    # Submit higher score
    score2_response = integration_client.post(
        "/api/game/score",
        json={"score": 250, "mode": "walls"},
        headers=auth_headers_integration,
    )

    assert score2_response.status_code == 201
    score2_data = score2_response.json()
    assert score2_data["isNewHighScore"] is True

    # Get leaderboard
    leaderboard_response = integration_client.get("/api/game/leaderboard?mode=walls")

    assert leaderboard_response.status_code == 200
    leaderboard_data = leaderboard_response.json()
    assert leaderboard_data["total"] >= 1
    assert len(leaderboard_data["entries"]) >= 1

    # Verify user is in leaderboard
    user_entry = next(
        (
            entry
            for entry in leaderboard_data["entries"]
            if entry["username"] == "integrationuser"
        ),
        None,
    )
    assert user_entry is not None
    assert user_entry["score"] == 250  # Should show latest score


def test_player_profile_flow(integration_client, auth_headers_integration):
    """Test player profile reflects game statistics."""
    # Get initial profile
    profile_response = integration_client.get(
        "/api/player/profile", headers=auth_headers_integration
    )

    assert profile_response.status_code == 200
    initial_profile = profile_response.json()
    assert initial_profile["username"] == "integrationuser"
    initial_games_played = initial_profile["gamesPlayed"]

    # Play some games
    integration_client.post(
        "/api/game/score",
        json={"score": 100, "mode": "walls"},
        headers=auth_headers_integration,
    )
    integration_client.post(
        "/api/game/score",
        json={"score": 200, "mode": "passthrough"},
        headers=auth_headers_integration,
    )

    # Get updated profile
    updated_response = integration_client.get(
        "/api/player/profile", headers=auth_headers_integration
    )

    assert updated_response.status_code == 200
    updated_profile = updated_response.json()
    assert updated_profile["gamesPlayed"] == initial_games_played + 2
    assert updated_profile["highScore"] == 200


def test_multi_user_leaderboard(integration_client):
    """Test leaderboard with multiple users competing."""
    # Create and play as first user
    user1_signup = integration_client.post(
        "/api/auth/signup",
        json={
            "email": "racer1@example.com",
            "username": "racer1",
            "password": "pass1234",
        },
    )
    user1_token = user1_signup.json()["token"]

    integration_client.post(
        "/api/game/score",
        json={"score": 300, "mode": "walls"},
        headers={"Authorization": f"Bearer {user1_token}"},
    )

    # Create and play as second user
    user2_signup = integration_client.post(
        "/api/auth/signup",
        json={
            "email": "racer2@example.com",
            "username": "racer2",
            "password": "pass1234",
        },
    )
    user2_token = user2_signup.json()["token"]

    integration_client.post(
        "/api/game/score",
        json={"score": 500, "mode": "walls"},
        headers={"Authorization": f"Bearer {user2_token}"},
    )

    # Create and play as third user
    user3_signup = integration_client.post(
        "/api/auth/signup",
        json={
            "email": "racer3@example.com",
            "username": "racer3",
            "password": "pass1234",
        },
    )
    user3_token = user3_signup.json()["token"]

    integration_client.post(
        "/api/game/score",
        json={"score": 400, "mode": "walls"},
        headers={"Authorization": f"Bearer {user3_token}"},
    )

    # Get leaderboard
    leaderboard_response = integration_client.get(
        "/api/game/leaderboard?mode=walls&limit=10"
    )

    assert leaderboard_response.status_code == 200
    leaderboard_data = leaderboard_response.json()

    # Find our three racers in the leaderboard
    entries = leaderboard_data["entries"]
    racer1 = next(e for e in entries if e["username"] == "racer1")
    racer2 = next(e for e in entries if e["username"] == "racer2")
    racer3 = next(e for e in entries if e["username"] == "racer3")

    # Verify scores
    assert racer2["score"] == 500
    assert racer3["score"] == 400
    assert racer1["score"] == 300

    # Verify rankings (racer2 should be highest)
    assert racer2["rank"] < racer3["rank"]
    assert racer3["rank"] < racer1["rank"]


def test_score_submission_updates_leaderboard_immediately(
    integration_client, auth_headers_integration
):
    """Test that score submission immediately updates leaderboard."""
    # Get initial leaderboard state
    initial_response = integration_client.get("/api/game/leaderboard?mode=passthrough")
    initial_total = initial_response.json()["total"]

    # Submit score
    integration_client.post(
        "/api/game/score",
        json={"score": 750, "mode": "passthrough"},
        headers=auth_headers_integration,
    )

    # Get updated leaderboard
    updated_response = integration_client.get("/api/game/leaderboard?mode=passthrough")
    updated_data = updated_response.json()

    # Should have one more entry
    assert updated_data["total"] == initial_total + 1

    # Verify the score is in the leaderboard
    user_entry = next(
        (
            entry
            for entry in updated_data["entries"]
            if entry["username"] == "integrationuser"
        ),
        None,
    )
    assert user_entry is not None
    assert user_entry["score"] == 750


def test_unauthorized_score_submission(integration_client):
    """Test that score submission requires authentication."""
    response = integration_client.post(
        "/api/game/score", json={"score": 100, "mode": "walls"}
    )

    assert response.status_code == 401


def test_unauthorized_profile_access(integration_client):
    """Test that profile access requires authentication."""
    response = integration_client.get("/api/player/profile")

    assert response.status_code == 401


def test_leaderboard_pagination_integration(integration_client):
    """Test leaderboard pagination with real data."""
    # Create 5 users with scores
    for i in range(5):
        signup = integration_client.post(
            "/api/auth/signup",
            json={
                "email": f"page{i}@example.com",
                "username": f"page{i}",
                "password": "pass1234",
            },
        )
        token = signup.json()["token"]

        integration_client.post(
            "/api/game/score",
            json={"score": (i + 1) * 100, "mode": "walls"},
            headers={"Authorization": f"Bearer {token}"},
        )

    # Get first page
    page1_response = integration_client.get(
        "/api/game/leaderboard?mode=walls&limit=2&offset=0"
    )
    page1_data = page1_response.json()

    assert len(page1_data["entries"]) == 2
    assert page1_data["total"] >= 5

    # Get second page
    page2_response = integration_client.get(
        "/api/game/leaderboard?mode=walls&limit=2&offset=2"
    )
    page2_data = page2_response.json()

    assert len(page2_data["entries"]) == 2
    assert page2_data["total"] >= 5

    # Entries should be different
    page1_usernames = {e["username"] for e in page1_data["entries"]}
    page2_usernames = {e["username"] for e in page2_data["entries"]}
    assert len(page1_usernames.intersection(page2_usernames)) == 0
