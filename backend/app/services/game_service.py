"""
Game service - Business logic for game operations.
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.database import Database
from app.models import GameMode, LeaderboardEntry, LeaderboardResponse, LiveGame, ScoreResponse


class GameService:
    """Service for game operations."""
    
    @staticmethod
    def submit_score(user_id: str, score: int, mode: GameMode, db: Session) -> ScoreResponse:
        """
        Submit a game score for a user.
        
        Args:
            user_id: User ID
            score: Score value
            mode: Game mode
            db: Database session
        
        Raises:
            ValueError: If player not found
        """
        database = Database(db)
        result = database.add_score(user_id, score, mode)
        
        return ScoreResponse(
            message="Score submitted successfully",
            is_new_high_score=result["is_new_high_score"],
            rank=result["rank"]
        )
    
    @staticmethod
    def get_leaderboard(
        mode: Optional[GameMode] = None,
        limit: int = 10,
        offset: int = 0,
        db: Session = None
    ) -> LeaderboardResponse:
        """
        Get leaderboard rankings.
        
        Args:
            mode: Optional game mode filter
            limit: Number of entries
            offset: Offset for pagination
            db: Database session
        """
        database = Database(db)
        entries_data, total = database.get_leaderboard(mode, limit, offset)
        
        entries = [LeaderboardEntry(**entry) for entry in entries_data]
        
        return LeaderboardResponse(entries=entries, total=total)
    
    @staticmethod
    def get_live_games(
        mode: Optional[GameMode] = None,
        limit: int = 10,
        db: Session = None
    ) -> list[LiveGame]:
        """
        Get currently active live games.
        
        Args:
            mode: Optional game mode filter
            limit: Number of games
            db: Database session
        """
        database = Database(db)
        games_data = database.get_live_games(mode, limit)
        
        return [LiveGame(**game) for game in games_data]
