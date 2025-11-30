"""
Player service - Business logic for player operations.
"""
from typing import Optional
from app.database import db
from app.models import Player


class PlayerService:
    """Service for player operations."""
    
    @staticmethod
    def get_profile(user_id: str) -> Optional[Player]:
        """
        Get player profile and statistics.
        
        Returns:
            Player object or None if not found
        """
        player_data = db.get_player(user_id)
        
        if not player_data:
            return None
        
        return Player(**player_data)
