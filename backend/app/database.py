"""
Database session management and repository using SQLAlchemy.
Provides same interface as the previous MockDatabase for compatibility with services.
"""

from datetime import datetime, timedelta, UTC
from typing import Optional, Generator
import uuid
import bcrypt

from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.config import settings
from app.db_models import Base, User, Player, Score
from app.models import GameMode


# Create engine with appropriate configuration
if settings.database_url.startswith("sqlite"):
    # SQLite configuration
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.database_echo,
    )
else:
    # PostgreSQL configuration
    engine = create_engine(
        settings.database_url,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
        echo=settings.database_echo,
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Drop all database tables (use with caution!)."""
    Base.metadata.drop_all(bind=engine)


class Database:
    """
    Database repository class.
    Maintains same interface as MockDatabase for service compatibility.
    """

    def __init__(self, session: Optional[Session] = None):
        """
        Initialize database repository.

        Args:
            session: Optional SQLAlchemy session. If None, creates a new one.
        """
        self._session = session
        self._owns_session = session is None

    @property
    def session(self) -> Session:
        """Get or create session."""
        if self._session is None:
            self._session = SessionLocal()
        return self._session

    def close(self):
        """Close session if we own it."""
        if self._owns_session and self._session:
            self._session.close()
            self._session = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    # User operations
    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email."""
        user = self.session.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()

        if not user:
            return None

        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "password_hash": user.password_hash,
        }

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID."""
        user = self.session.execute(
            select(User).where(User.id == user_id)
        ).scalar_one_or_none()

        if not user:
            return None

        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "password_hash": user.password_hash,
        }

    def create_user(self, email: str, username: str, password: str) -> dict:
        """Create a new user."""
        # Check if email already exists
        existing_email = self.session.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()

        if existing_email:
            raise ValueError("Email already exists")

        # Check if username already exists
        existing_username = self.session.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()

        if existing_username:
            raise ValueError("Username already exists")

        # Hash password
        password_bytes = password.encode("utf-8")
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

        # Create user
        user_id = str(uuid.uuid4())
        user = User(
            id=user_id,
            email=email,
            username=username,
            password_hash=hashed.decode("utf-8"),
        )
        self.session.add(user)

        # Create player profile
        player = Player(
            id=user_id, username=username, score=0, high_score=0, games_played=0
        )
        self.session.add(player)

        self.session.commit()

        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "password_hash": user.password_hash,
        }

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        password_bytes = plain_password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    # Player operations
    def get_player(self, user_id: str) -> Optional[dict]:
        """Get player profile."""
        player = self.session.execute(
            select(Player).where(Player.id == user_id)
        ).scalar_one_or_none()

        if not player:
            return None

        return {
            "id": player.id,
            "username": player.username,
            "score": player.score,
            "high_score": player.high_score,
            "games_played": player.games_played,
        }

    # Score operations
    def add_score(self, user_id: str, score: int, mode: GameMode) -> dict:
        """Add a score for a user."""
        player = self.session.execute(
            select(Player).where(Player.id == user_id)
        ).scalar_one_or_none()

        if not player:
            raise ValueError("Player not found")

        # Update player stats
        player.games_played += 1
        is_new_high_score = score > player.high_score
        if is_new_high_score:
            player.high_score = score

        # Add score record
        score_record = Score(
            user_id=user_id, username=player.username, score=score, mode=mode
        )
        self.session.add(score_record)

        self.session.commit()

        # Calculate rank
        rank = self.get_rank(score, mode)

        return {
            "is_new_high_score": is_new_high_score,
            "rank": rank,
        }

    def get_rank(self, score: int, mode: GameMode) -> int:
        """Calculate rank for a score."""
        # Count scores higher than this one in the same mode
        # Group by user, take max score per user
        subquery = (
            select(Score.user_id, func.max(Score.score).label("max_score"))
            .where(Score.mode == mode)
            .group_by(Score.user_id)
            .subquery()
        )

        higher_scores = self.session.execute(
            select(func.count())
            .select_from(subquery)
            .where(subquery.c.max_score > score)
        ).scalar()

        return higher_scores + 1

    def get_leaderboard(
        self, mode: Optional[GameMode] = None, limit: int = 10, offset: int = 0
    ) -> tuple[list[dict], int]:
        """Get leaderboard entries."""
        # Build query for best score per user
        query = select(
            Score.user_id,
            Score.username,
            func.max(Score.score).label("max_score"),
            func.max(Score.created_at).label("latest_date"),
        )

        # Filter by mode if specified
        if mode:
            query = query.where(Score.mode == mode)

        # Group by user
        query = query.group_by(Score.user_id, Score.username)

        # Get all results to sort and paginate
        results = self.session.execute(query).all()

        # Sort by score descending
        sorted_results = sorted(results, key=lambda x: x.max_score, reverse=True)

        # Paginate
        total = len(sorted_results)
        paginated_results = sorted_results[offset : offset + limit]

        # Build entries with rank
        entries = []
        for rank, result in enumerate(paginated_results, start=offset + 1):
            entries.append(
                {
                    "rank": rank,
                    "username": result.username,
                    "score": result.max_score,
                    "date": result.latest_date,
                }
            )

        return entries, total

    # Live game operations (mock for now)
    def get_live_games(
        self, mode: Optional[GameMode] = None, limit: int = 10
    ) -> list[dict]:
        """Get live games (returns empty list for now)."""
        # Live games would require a real-time WebSocket implementation
        # For now, return empty list to maintain compatibility
        return []


# Global database instance for backwards compatibility
db = Database()


def seed_db():
    """Seed database with mock players and scores."""
    with Database() as database:
        mock_players_data = [
            # Top players
            {
                "username": "SnakeMaster",
                "email": "snake@example.com",
                "high_score": 450,
                "games_played": 89,
                "mode": GameMode.WALLS,
            },
            {
                "username": "NeonViper",
                "email": "neon@example.com",
                "high_score": 380,
                "games_played": 67,
                "mode": GameMode.WALLS,
            },
            {
                "username": "GridRunner",
                "email": "grid@example.com",
                "high_score": 420,
                "games_played": 54,
                "mode": GameMode.PASSTHROUGH,
            },
            {
                "username": "ArcadeKing",
                "email": "arcade@example.com",
                "high_score": 290,
                "games_played": 45,
                "mode": GameMode.WALLS,
            },
            {
                "username": "PixelHunter",
                "email": "pixel@example.com",
                "high_score": 350,
                "games_played": 38,
                "mode": GameMode.PASSTHROUGH,
            },
            # Mid-tier players
            {
                "username": "SpeedDemon",
                "email": "speed@example.com",
                "high_score": 275,
                "games_played": 31,
                "mode": GameMode.WALLS,
            },
            {
                "username": "NinjaNoodle",
                "email": "ninja@example.com",
                "high_score": 310,
                "games_played": 42,
                "mode": GameMode.PASSTHROUGH,
            },
            {
                "username": "RetroGamer",
                "email": "retro@example.com",
                "high_score": 265,
                "games_played": 28,
                "mode": GameMode.WALLS,
            },
            {
                "username": "PixelPro",
                "email": "pixelpro@example.com",
                "high_score": 295,
                "games_played": 35,
                "mode": GameMode.PASSTHROUGH,
            },
            # New players
            {
                "username": "Beginner123",
                "email": "beginner@example.com",
                "high_score": 120,
                "games_played": 15,
                "mode": GameMode.WALLS,
            },
            {
                "username": "JustStarted",
                "email": "newbie@example.com",
                "high_score": 85,
                "games_played": 8,
                "mode": GameMode.WALLS,
            },
            {
                "username": "LearningSnake",
                "email": "learning@example.com",
                "high_score": 95,
                "games_played": 12,
                "mode": GameMode.PASSTHROUGH,
            },
        ]

        # Password for all demo users
        demo_password = "demo123"

        import random

        for data in mock_players_data:
            try:
                # Create user and player
                user_dict = database.create_user(
                    data["email"], data["username"], demo_password
                )
                user_id = user_dict["id"]

                # Update player stats
                player = database.session.execute(
                    select(Player).where(Player.id == user_id)
                ).scalar_one()

                player.high_score = data["high_score"]
                player.games_played = data["games_played"]

                # Add high score
                high_score_record = Score(
                    user_id=user_id,
                    username=data["username"],
                    score=data["high_score"],
                    mode=data["mode"],
                    created_at=datetime.now(UTC)
                    - timedelta(days=int(7 * (1 - data["high_score"] / 500))),
                )
                database.session.add(high_score_record)

                # Add some historical scores
                for _ in range(random.randint(2, 5)):
                    past_score = int(data["high_score"] * random.uniform(0.4, 0.9))
                    past_score_record = Score(
                        user_id=user_id,
                        username=data["username"],
                        score=past_score,
                        mode=data["mode"],
                        created_at=datetime.now(UTC)
                        - timedelta(days=random.randint(1, 30)),
                    )
                    database.session.add(past_score_record)

                database.session.commit()

            except ValueError:
                # User already exists, skip
                database.session.rollback()
                continue

        print(f"✅ Database seeded with {len(mock_players_data)} players")
