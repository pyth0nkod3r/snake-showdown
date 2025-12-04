"""
Integration tests for database operations.
Tests the Database class with actual SQLite database to verify CRUD operations,
score management, and leaderboard queries.
"""

import pytest
from app.database import Database
from app.models import GameMode


def test_create_user(integration_db_session):
    """Test creating a new user in the database."""
    db = Database(integration_db_session)

    user = db.create_user(
        email="test@example.com", username="testuser", password="testpass123"
    )

    assert user is not None
    assert user["email"] == "test@example.com"
    assert user["username"] == "testuser"
    assert user["id"] is not None
    assert "password_hash" in user
    assert user["password_hash"] != "testpass123"  # Should be hashed


def test_create_duplicate_email(integration_db_session):
    """Test that creating a user with duplicate email raises error."""
    db = Database(integration_db_session)

    db.create_user(email="duplicate@example.com", username="user1", password="pass123")

    with pytest.raises(ValueError, match="Email already exists"):
        db.create_user(
            email="duplicate@example.com", username="user2", password="pass456"
        )


def test_create_duplicate_username(integration_db_session):
    """Test that creating a user with duplicate username raises error."""
    db = Database(integration_db_session)

    db.create_user(email="user1@example.com", username="duplicate", password="pass123")

    with pytest.raises(ValueError, match="Username already exists"):
        db.create_user(
            email="user2@example.com", username="duplicate", password="pass456"
        )


def test_get_user_by_email(integration_db_session):
    """Test retrieving a user by email."""
    db = Database(integration_db_session)

    # Create user
    created_user = db.create_user(
        email="retrieve@example.com", username="retrieveuser", password="pass123"
    )

    # Retrieve user
    user = db.get_user_by_email("retrieve@example.com")

    assert user is not None
    assert user["id"] == created_user["id"]
    assert user["email"] == "retrieve@example.com"
    assert user["username"] == "retrieveuser"


def test_get_user_by_email_not_found(integration_db_session):
    """Test retrieving a non-existent user by email returns None."""
    db = Database(integration_db_session)

    user = db.get_user_by_email("nonexistent@example.com")

    assert user is None


def test_get_user_by_id(integration_db_session):
    """Test retrieving a user by ID."""
    db = Database(integration_db_session)

    # Create user
    created_user = db.create_user(
        email="byid@example.com", username="byiduser", password="pass123"
    )

    # Retrieve user
    user = db.get_user_by_id(created_user["id"])

    assert user is not None
    assert user["id"] == created_user["id"]
    assert user["email"] == "byid@example.com"


def test_verify_password_correct(integration_db_session):
    """Test password verification with correct password."""
    db = Database(integration_db_session)

    user = db.create_user(
        email="verify@example.com", username="verifyuser", password="correctpass"
    )

    assert db.verify_password("correctpass", user["password_hash"]) is True


def test_verify_password_incorrect(integration_db_session):
    """Test password verification with incorrect password."""
    db = Database(integration_db_session)

    user = db.create_user(
        email="verify2@example.com", username="verifyuser2", password="correctpass"
    )

    assert db.verify_password("wrongpass", user["password_hash"]) is False


def test_get_player_profile(integration_db_session):
    """Test retrieving player profile."""
    db = Database(integration_db_session)

    # Create user (which also creates player profile)
    user = db.create_user(
        email="player@example.com", username="playeruser", password="pass123"
    )

    # Get player profile
    player = db.get_player(user["id"])

    assert player is not None
    assert player["username"] == "playeruser"
    assert player["score"] == 0
    assert player["high_score"] == 0
    assert player["games_played"] == 0


def test_add_score(integration_db_session):
    """Test adding a score for a user."""
    db = Database(integration_db_session)

    # Create user
    user = db.create_user(
        email="score@example.com", username="scoreuser", password="pass123"
    )

    # Add score
    result = db.add_score(user["id"], 100, GameMode.WALLS)

    assert result["is_new_high_score"] is True
    assert result["rank"] >= 1

    # Verify player profile updated
    player = db.get_player(user["id"])
    assert player["high_score"] == 100
    assert player["games_played"] == 1


def test_add_multiple_scores(integration_db_session):
    """Test adding multiple scores updates player stats correctly."""
    db = Database(integration_db_session)

    user = db.create_user(
        email="multiscore@example.com", username="multiscoreuser", password="pass123"
    )

    # Add first score
    db.add_score(user["id"], 50, GameMode.WALLS)

    # Add second higher score
    result = db.add_score(user["id"], 150, GameMode.WALLS)

    assert result["is_new_high_score"] is True

    # Add third lower score
    result = db.add_score(user["id"], 75, GameMode.PASSTHROUGH)

    assert result["is_new_high_score"] is False

    # Verify player profile
    player = db.get_player(user["id"])
    assert player["high_score"] == 150  # Highest score
    assert player["games_played"] == 3


def test_get_rank(integration_db_session):
    """Test rank calculation for a score."""
    db = Database(integration_db_session)

    # Create multiple users with scores
    user1 = db.create_user("user1@example.com", "user1", "pass")
    user2 = db.create_user("user2@example.com", "user2", "pass")
    user3 = db.create_user("user3@example.com", "user3", "pass")

    db.add_score(user1["id"], 100, GameMode.WALLS)
    db.add_score(user2["id"], 200, GameMode.WALLS)
    db.add_score(user3["id"], 150, GameMode.WALLS)

    # Test rank for different scores
    rank_250 = db.get_rank(250, GameMode.WALLS)
    rank_175 = db.get_rank(175, GameMode.WALLS)
    rank_50 = db.get_rank(50, GameMode.WALLS)

    assert rank_250 == 1  # Highest score
    assert rank_175 == 2  # Between 200 and 150
    assert rank_50 == 4  # Lowest score


def test_get_leaderboard(integration_db_session):
    """Test retrieving leaderboard entries."""
    db = Database(integration_db_session)

    # Create users and scores
    user1 = db.create_user("lead1@example.com", "leader1", "pass")
    user2 = db.create_user("lead2@example.com", "leader2", "pass")
    user3 = db.create_user("lead3@example.com", "leader3", "pass")

    db.add_score(user1["id"], 300, GameMode.WALLS)
    db.add_score(user2["id"], 500, GameMode.WALLS)
    db.add_score(user3["id"], 400, GameMode.WALLS)

    # Get leaderboard
    entries, total = db.get_leaderboard(mode=GameMode.WALLS, limit=10, offset=0)

    assert total == 3
    assert len(entries) == 3

    # Verify order (highest to lowest)
    assert entries[0]["score"] == 500
    assert entries[0]["username"] == "leader2"
    assert entries[0]["rank"] == 1

    assert entries[1]["score"] == 400
    assert entries[1]["username"] == "leader3"
    assert entries[1]["rank"] == 2

    assert entries[2]["score"] == 300
    assert entries[2]["username"] == "leader1"
    assert entries[2]["rank"] == 3


def test_get_leaderboard_pagination(integration_db_session):
    """Test leaderboard pagination."""
    db = Database(integration_db_session)

    # Create 5 users with scores
    for i in range(5):
        user = db.create_user(f"page{i}@example.com", f"page{i}", "pass")
        db.add_score(user["id"], (i + 1) * 100, GameMode.WALLS)

    # Get first page (2 entries)
    entries, total = db.get_leaderboard(mode=GameMode.WALLS, limit=2, offset=0)

    assert total == 5
    assert len(entries) == 2
    assert entries[0]["score"] == 500  # Highest

    # Get second page
    entries, total = db.get_leaderboard(mode=GameMode.WALLS, limit=2, offset=2)

    assert total == 5
    assert len(entries) == 2
    assert entries[0]["score"] == 300


def test_get_leaderboard_mode_filter(integration_db_session):
    """Test leaderboard filtering by game mode."""
    db = Database(integration_db_session)

    user1 = db.create_user("mode1@example.com", "modeuser1", "pass")
    user2 = db.create_user("mode2@example.com", "modeuser2", "pass")

    # Add scores in different modes
    db.add_score(user1["id"], 100, GameMode.WALLS)
    db.add_score(user2["id"], 200, GameMode.PASSTHROUGH)

    # Get leaderboard for WALLS mode only
    entries, total = db.get_leaderboard(mode=GameMode.WALLS, limit=10, offset=0)

    assert total == 1
    assert len(entries) == 1
    assert entries[0]["username"] == "modeuser1"

    # Get leaderboard for all modes
    entries, total = db.get_leaderboard(mode=None, limit=10, offset=0)

    assert total == 2
    assert len(entries) == 2


def test_get_live_games(integration_db_session):
    """Test getting live games (currently returns empty list)."""
    db = Database(integration_db_session)

    games = db.get_live_games(mode=None, limit=10)

    assert isinstance(games, list)
    assert len(games) == 0
