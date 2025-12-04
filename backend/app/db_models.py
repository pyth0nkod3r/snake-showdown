"""
SQLAlchemy database models (ORM).
"""
from datetime import datetime, UTC
from typing import Optional
import uuid

from sqlalchemy import String, Integer, DateTime, Enum, ForeignKey, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.models import GameMode


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class User(Base):
    """User account model."""
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    
    # Relationships
    player: Mapped[Optional["Player"]] = relationship("Player", back_populates="user", uselist=False, cascade="all, delete-orphan")
    scores: Mapped[list["Score"]] = relationship("Score", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class Player(Base):
    """Player profile model."""
    __tablename__ = "players"
    
    id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    high_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="player")
    
    # Index for high score queries
    __table_args__ = (
        Index('idx_high_score', 'high_score'),
    )
    
    def __repr__(self) -> str:
        return f"<Player(id={self.id}, username={self.username}, high_score={self.high_score})>"


class Score(Base):
    """Score record model."""
    __tablename__ = "scores"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    username: Mapped[str] = mapped_column(String(20), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[GameMode] = mapped_column(Enum(GameMode), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="scores")
    
    # Indexes for leaderboard queries
    __table_args__ = (
        Index('idx_user_scores', 'user_id', 'score'),
        Index('idx_mode_scores', 'mode', 'score'),
        Index('idx_score_date', 'score', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<Score(id={self.id}, username={self.username}, score={self.score}, mode={self.mode})>"
