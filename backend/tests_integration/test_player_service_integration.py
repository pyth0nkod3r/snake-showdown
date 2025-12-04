"""
Integration tests for PlayerService.
Tests player service with real database operations.
"""

from app.services.player_service import PlayerService
from app.services.auth_service import AuthService
from app.services.game_service import GameService
from app.models import GameMode, Player


def test_get_profile_after_signup(integration_db_session):
    """Test getting player profile immediately after signup."""
    # Create user
    user_response = AuthService.signup(
        email="profile@example.com",
        username="profileuser",
        password="pass123",
        db=integration_db_session,
    )

    # Get profile
    player = PlayerService.get_profile(
        user_id=user_response.user.id, db=integration_db_session
    )

    assert player is not None
    assert isinstance(player, Player)
    assert player.username == "profileuser"
    assert player.score == 0
    assert player.high_score == 0
    assert player.games_played == 0


def test_get_profile_nonexistent_user(integration_db_session):
    """Test getting profile for non-existent user returns None."""
    player = PlayerService.get_profile(
        user_id="nonexistent-id", db=integration_db_session
    )

    assert player is None


def test_get_profile_after_playing_games(integration_db_session):
    """Test that profile reflects game statistics correctly."""
    # Create user
    user_response = AuthService.signup(
        email="stats@example.com",
        username="statsuser",
        password="pass123",
        db=integration_db_session,
    )
    user_id = user_response.user.id

    # Submit multiple scores
    GameService.submit_score(user_id, 100, GameMode.WALLS, integration_db_session)
    GameService.submit_score(user_id, 250, GameMode.WALLS, integration_db_session)
    GameService.submit_score(user_id, 150, GameMode.PASSTHROUGH, integration_db_session)

    # Get profile
    player = PlayerService.get_profile(user_id, integration_db_session)

    assert player is not None
    assert player.username == "statsuser"
    assert player.high_score == 250  # Highest score across all games
    assert player.games_played == 3


def test_profile_updates_with_new_high_score(integration_db_session):
    """Test that profile high score updates when new high score is achieved."""
    # Create user
    user_response = AuthService.signup(
        email="highscore@example.com",
        username="highscorer",
        password="pass123",
        db=integration_db_session,
    )
    user_id = user_response.user.id

    # Submit initial score
    GameService.submit_score(user_id, 100, GameMode.WALLS, integration_db_session)

    # Check profile
    player = PlayerService.get_profile(user_id, integration_db_session)
    assert player.high_score == 100

    # Submit higher score
    GameService.submit_score(user_id, 300, GameMode.WALLS, integration_db_session)

    # Check profile again
    player = PlayerService.get_profile(user_id, integration_db_session)
    assert player.high_score == 300
    assert player.games_played == 2


def test_profile_does_not_decrease_high_score(integration_db_session):
    """Test that high score doesn't decrease when lower scores are submitted."""
    # Create user
    user_response = AuthService.signup(
        email="keeper@example.com",
        username="keeper",
        password="pass123",
        db=integration_db_session,
    )
    user_id = user_response.user.id

    # Submit high score first
    GameService.submit_score(user_id, 500, GameMode.WALLS, integration_db_session)

    # Submit lower scores
    GameService.submit_score(user_id, 100, GameMode.WALLS, integration_db_session)
    GameService.submit_score(user_id, 200, GameMode.PASSTHROUGH, integration_db_session)

    # Check profile - high score should still be 500
    player = PlayerService.get_profile(user_id, integration_db_session)
    assert player.high_score == 500
    assert player.games_played == 3
