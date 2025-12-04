"""
Player service - Business logic for player operations.
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.database import Database
from app.models import Player


class PlayerService:
    """Service for player operations."""
    
    @staticmethod
    def get_profile(user_id: str, db: Session) -> Optional[Player]:
        """
        Get player profile and statistics.
        
        Args:
            user_id: User ID
            db: Database session
        
        Returns:
            Player object or None if not found
        """
        database = Database(db)
        player_data = database.get_player(user_id)
        
        if not player_data:
            return None
        
        return Player(**player_data)
