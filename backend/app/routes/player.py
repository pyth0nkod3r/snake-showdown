"""
Player route handlers.
"""
from fastapi import APIRouter, HTTPException, status, Depends

from app.models import Player, ErrorResponse
from app.services.player_service import PlayerService
from app.auth import get_current_user

router = APIRouter(prefix="/player", tags=["Player"])


@router.get(
    "/profile",
    response_model=Player,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    }
)
async def get_player_profile(current_user: dict = Depends(get_current_user)):
    """Get player profile and statistics."""
    player = PlayerService.get_profile(current_user["id"])
    
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player profile not found"
        )
    
    return player
