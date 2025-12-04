"""
Integration tests for GameService.
Tests game service with real database operations.
"""

from app.services.game_service import GameService
from app.services.auth_service import AuthService
from app.models import GameMode, ScoreResponse, LeaderboardResponse


def test_submit_score_success(integration_db_session):
    """Test successful score submission."""
    # Create user
    user_response = AuthService.signup(
        email="gamer@example.com",
        username="gamer",
        password="pass123",
        db=integration_db_session,
    )

    # Submit score
    response = GameService.submit_score(
        user_id=user_response.user.id,
        score=250,
        mode=GameMode.WALLS,
        db=integration_db_session,
    )

    assert isinstance(response, ScoreResponse)
    assert response.message == "Score submitted successfully"
    assert response.is_new_high_score is True
    assert response.rank >= 1


def test_submit_multiple_scores(integration_db_session):
    """Test submitting multiple scores updates high score correctly."""
    # Create user
    user_response = AuthService.signup(
        email="multiplay@example.com",
        username="multiplay",
        password="pass123",
        db=integration_db_session,
    )

    user_id = user_response.user.id

    # Submit first score
    response1 = GameService.submit_score(
        user_id=user_id, score=100, mode=GameMode.WALLS, db=integration_db_session
    )
    assert response1.is_new_high_score is True

    # Submit higher score
    response2 = GameService.submit_score(
        user_id=user_id, score=200, mode=GameMode.WALLS, db=integration_db_session
    )
    assert response2.is_new_high_score is True

    # Submit lower score
    response3 = GameService.submit_score(
        user_id=user_id, score=150, mode=GameMode.WALLS, db=integration_db_session
    )
    assert response3.is_new_high_score is False


def test_get_leaderboard_empty(integration_db_session):
    """Test getting leaderboard when no scores exist."""
    response = GameService.get_leaderboard(
        mode=None, limit=10, offset=0, db=integration_db_session
    )

    assert isinstance(response, LeaderboardResponse)
    assert len(response.entries) == 0
    assert response.total == 0


def test_get_leaderboard_with_scores(integration_db_session):
    """Test getting leaderboard with multiple scores."""
    # Create multiple users and submit scores
    users = []
    for i in range(3):
        user_response = AuthService.signup(
            email=f"player{i}@example.com",
            username=f"player{i}",
            password="pass123",
            db=integration_db_session,
        )
        users.append(user_response.user.id)

    # Submit scores in different orders
    GameService.submit_score(users[0], 300, GameMode.WALLS, integration_db_session)
    GameService.submit_score(users[1], 500, GameMode.WALLS, integration_db_session)
    GameService.submit_score(users[2], 400, GameMode.WALLS, integration_db_session)

    # Get leaderboard
    response = GameService.get_leaderboard(
        mode=GameMode.WALLS, limit=10, offset=0, db=integration_db_session
    )

    assert response.total == 3
    assert len(response.entries) == 3

    # Verify order (highest to lowest)
    assert response.entries[0].score == 500
    assert response.entries[0].username == "player1"
    assert response.entries[0].rank == 1

    assert response.entries[1].score == 400
    assert response.entries[1].username == "player2"
    assert response.entries[1].rank == 2

    assert response.entries[2].score == 300
    assert response.entries[2].username == "player0"
    assert response.entries[2].rank == 3


def test_get_leaderboard_pagination(integration_db_session):
    """Test leaderboard pagination."""
    # Create 5 users with scores
    for i in range(5):
        user_response = AuthService.signup(
            email=f"paged{i}@example.com",
            username=f"paged{i}",
            password="pass123",
            db=integration_db_session,
        )
        GameService.submit_score(
            user_response.user.id, (i + 1) * 100, GameMode.WALLS, integration_db_session
        )

    # Get first page
    response = GameService.get_leaderboard(
        mode=GameMode.WALLS, limit=2, offset=0, db=integration_db_session
    )

    assert response.total == 5
    assert len(response.entries) == 2
    assert response.entries[0].score == 500

    # Get second page
    response = GameService.get_leaderboard(
        mode=GameMode.WALLS, limit=2, offset=2, db=integration_db_session
    )

    assert response.total == 5
    assert len(response.entries) == 2
    assert response.entries[0].score == 300


def test_get_leaderboard_mode_filter(integration_db_session):
    """Test leaderboard filtering by game mode."""
    # Create user
    user_response = AuthService.signup(
        email="modetest@example.com",
        username="modetest",
        password="pass123",
        db=integration_db_session,
    )
    user_id = user_response.user.id

    # Submit scores in different modes
    GameService.submit_score(user_id, 100, GameMode.WALLS, integration_db_session)
    GameService.submit_score(user_id, 200, GameMode.PASSTHROUGH, integration_db_session)

    # Get WALLS leaderboard
    walls_response = GameService.get_leaderboard(
        mode=GameMode.WALLS, limit=10, offset=0, db=integration_db_session
    )

    assert walls_response.total == 1
    assert walls_response.entries[0].score == 100

    # Get all modes leaderboard - shows best score per user across all modes
    # Since this is the same user, still only 1 entry with the higher score
    all_response = GameService.get_leaderboard(
        mode=None, limit=10, offset=0, db=integration_db_session
    )

    assert all_response.total == 1
    assert all_response.entries[0].score == 200  # Higher score across all modes


def test_get_live_games(integration_db_session):
    """Test getting live games (currently returns empty list)."""
    games = GameService.get_live_games(mode=None, limit=10, db=integration_db_session)

    assert isinstance(games, list)
    assert len(games) == 0


def test_rank_calculation_with_ties(integration_db_session):
    """Test rank calculation when multiple users have same score."""
    # Create users with same scores
    for i in range(3):
        user_response = AuthService.signup(
            email=f"tie{i}@example.com",
            username=f"tie{i}",
            password="pass123",
            db=integration_db_session,
        )
        GameService.submit_score(
            user_response.user.id,
            100,  # Same score for all
            GameMode.WALLS,
            integration_db_session,
        )

    # Add one user with higher score
    user_response = AuthService.signup(
        email="higher@example.com",
        username="higher",
        password="pass123",
        db=integration_db_session,
    )
    response = GameService.submit_score(
        user_response.user.id, 200, GameMode.WALLS, integration_db_session
    )

    # Should be rank 1 since it's the highest
    assert response.rank == 1
