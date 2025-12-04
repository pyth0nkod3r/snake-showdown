"""
Game route handlers.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session

from app.models import (
    ScoreSubmission,
    ScoreResponse,
    LeaderboardResponse,
    LiveGame,
    GameMode,
    ErrorResponse,
)
from app.services.game_service import GameService
from app.auth import get_current_user
from app.database import get_db

router = APIRouter(prefix="/game", tags=["Game"])


@router.post(
    "/score",
    response_model=ScoreResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
    }
)
async def submit_score(
    submission: ScoreSubmission,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit a game score."""
    try:
        return GameService.submit_score(current_user["id"], submission.score, submission.mode, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/leaderboard",
    response_model=LeaderboardResponse,
    responses={
        400: {"model": ErrorResponse},
    }
)
async def get_leaderboard(
    mode: Optional[GameMode] = Query(None, description="Filter by game mode"),
    limit: int = Query(10, ge=1, le=100, description="Maximum entries to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: Session = Depends(get_db)
):
    """Get leaderboard rankings."""
    return GameService.get_leaderboard(mode, limit, offset, db)


@router.get(
    "/live",
    response_model=list[LiveGame],
    responses={
        400: {"model": ErrorResponse},
    }
)
async def get_live_games(
    mode: Optional[GameMode] = Query(None, description="Filter by game mode"),
    limit: int = Query(10, ge=1, le=50, description="Maximum games to return"),
    db: Session = Depends(get_db)
):
    """Get currently active live games."""
    return GameService.get_live_games(mode, limit, db)
