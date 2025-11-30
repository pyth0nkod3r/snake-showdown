"""
Game service - Business logic for game operations.
"""
from typing import Optional
from app.database import db
from app.models import GameMode, LeaderboardEntry, LeaderboardResponse, LiveGame, ScoreResponse


class GameService:
    """Service for game operations."""
    
    @staticmethod
    def submit_score(user_id: str, score: int, mode: GameMode) -> ScoreResponse:
        """
        Submit a game score for a user.
        
        Raises:
            ValueError: If player not found
        """
        result = db.add_score(user_id, score, mode)
        
        return ScoreResponse(
            message="Score submitted successfully",
            is_new_high_score=result["is_new_high_score"],
            rank=result["rank"]
        )
    
    @staticmethod
    def get_leaderboard(
        mode: Optional[GameMode] = None,
        limit: int = 10,
        offset: int = 0
    ) -> LeaderboardResponse:
        """Get leaderboard rankings."""
        entries_data, total = db.get_leaderboard(mode, limit, offset)
        
        entries = [LeaderboardEntry(**entry) for entry in entries_data]
        
        return LeaderboardResponse(entries=entries, total=total)
    
    @staticmethod
    def get_live_games(
        mode: Optional[GameMode] = None,
        limit: int = 10
    ) -> list[LiveGame]:
        """Get currently active live games."""
        games_data = db.get_live_games(mode, limit)
        
        return [LiveGame(**game) for game in games_data]
