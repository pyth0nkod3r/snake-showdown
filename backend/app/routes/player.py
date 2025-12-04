"""
Player route handlers.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.models import Player, ErrorResponse
from app.services.player_service import PlayerService
from app.auth import get_current_user
from app.database import get_db

router = APIRouter(prefix="/player", tags=["Player"])


@router.get(
    "/profile",
    response_model=Player,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    }
)
async def get_player_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get player profile and statistics."""
    player = PlayerService.get_profile(current_user["id"], db)
    
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player profile not found"
        )
    
    return player
