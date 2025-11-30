"""
Pydantic models for API request/response validation.
Based on OpenAPI specification.
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class GameMode(str, Enum):
    """Game mode type."""
    WALLS = "walls"
    PASSTHROUGH = "passthrough"


class Direction(str, Enum):
    """Snake direction."""
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Position(BaseModel):
    """Grid position."""
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    
    model_config = ConfigDict(from_attributes=True)


class Snake(BaseModel):
    """Snake data."""
    body: list[Position] = Field(min_length=1)
    direction: Direction
    
    model_config = ConfigDict(from_attributes=True)


class GameState(BaseModel):
    """Complete game state."""
    snake: Snake
    food: Position
    score: int = Field(ge=0)
    is_game_over: bool = Field(alias="isGameOver")
    is_paused: bool = Field(alias="isPaused")
    mode: GameMode
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# Auth Models
class SignupRequest(BaseModel):
    """User signup request."""
    email: EmailStr
    password: str = Field(min_length=8)
    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")


class LoginRequest(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class AuthUser(BaseModel):
    """Authenticated user response."""
    id: str
    username: str
    email: str
    
    model_config = ConfigDict(from_attributes=True)


class AuthResponse(BaseModel):
    """Authentication response with token."""
    user: AuthUser
    token: str


# Player Models
class Player(BaseModel):
    """Player profile with statistics."""
    id: str
    username: str
    score: int = Field(ge=0, default=0)
    high_score: int = Field(ge=0, alias="highScore")
    games_played: int = Field(ge=0, alias="gamesPlayed")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# Game Models
class ScoreSubmission(BaseModel):
    """Score submission request."""
    score: int = Field(ge=0)
    mode: GameMode


class ScoreResponse(BaseModel):
    """Score submission response."""
    message: str
    is_new_high_score: bool = Field(alias="isNewHighScore")
    rank: int
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class LeaderboardEntry(BaseModel):
    """Leaderboard entry."""
    rank: int = Field(ge=1)
    username: str
    score: int = Field(ge=0)
    date: datetime
    
    model_config = ConfigDict(from_attributes=True)


class LeaderboardResponse(BaseModel):
    """Leaderboard response."""
    entries: list[LeaderboardEntry]
    total: int


class LiveGame(BaseModel):
    """Live game data."""
    id: str
    player: Player
    game_state: GameState = Field(alias="gameState")
    started_at: datetime = Field(alias="startedAt")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# Error Models
class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    message: str
    details: Optional[dict] = None
