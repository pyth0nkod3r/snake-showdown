"""
Mock database implementation.
This will be replaced with a real database later.
"""
from datetime import datetime, timedelta, UTC
from typing import Optional
import uuid
import bcrypt

from app.models import (
    GameMode,
    AuthUser,
    Player,
    LeaderboardEntry,
    LiveGame,
    GameState,
    Snake,
    Position,
    Direction,
)


class MockDatabase:
    """Mock in-memory database."""
    
    def __init__(self):
        """Initialize mock database with sample data."""
        self.users: dict[str, dict] = {}
        self.players: dict[str, dict] = {}
        self.scores: list[dict] = []
        self.live_games: list[dict] = []
        self._initialized = False
    
    def _ensure_initialized(self):
        """Ensure database is initialized with mock data."""
        if not self._initialized:
            self._add_mock_players()
            self._initialized = True
    
    def _add_mock_players(self):
        """Add mock players with scores."""
        mock_players_data = [
            {"username": "SnakeMaster", "email": "snake@example.com", "high_score": 450, "games_played": 89},
            {"username": "NeonViper", "email": "neon@example.com", "high_score": 380, "games_played": 67},
            {"username": "GridRunner", "email": "grid@example.com", "high_score": 320, "games_played": 54},
            {"username": "ArcadeKing", "email": "arcade@example.com", "high_score": 290, "games_played": 45},
            {"username": "PixelHunter", "email": "pixel@example.com", "high_score": 250, "games_played": 38},
        ]
        
       # Pre-computed bcrypt hash for password "demo123"
        demo_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5BI6iFz.y9P9u"
        
        for data in mock_players_data:
            user_id = str(uuid.uuid4())
            # Create user
            self.users[data["email"]] = {
                "id": user_id,
                "email": data["email"],
                "username": data["username"],
                "password_hash": demo_hash,
            }
            # Create player
            self.players[user_id] = {
                "id": user_id,
                "username": data["username"],
                "score": 0,
                "high_score": data["high_score"],
                "games_played": data["games_played"],
            }
            # Add score
            self.scores.append({
                "user_id": user_id,
                "username": data["username"],
                "score": data["high_score"],
                "mode": GameMode.WALLS,
                "date": datetime.now(UTC) - timedelta(days=int(7 * (1 - data["high_score"] / 500))),
            })
    
    # User operations
    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email."""
        self._ensure_initialized()
        return self.users.get(email)
    
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID."""
        self._ensure_initialized()
        for user in self.users.values():
            if user["id"] == user_id:
                return user
        return None
    
    def create_user(self, email: str, username: str, password: str) -> dict:
        """Create a new user."""
        # Check if email already exists
        if email in self.users:
            raise ValueError("Email already exists")
        
        # Check if username already exists
        for user in self.users.values():
            if user["username"] == username:
                raise ValueError("Username already exists")
        
        user_id = str(uuid.uuid4())
        # Hash password with bcrypt
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        
        user = {
            "id": user_id,
            "email": email,
            "username": username,
            "password_hash": hashed.decode('utf-8'),
        }
        self.users[email] = user
        
        # Create player profile
        self.players[user_id] = {
            "id": user_id,
            "username": username,
            "score": 0,
            "high_score": 0,
            "games_played": 0,
        }
        
        return user
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    
    # Player operations
    def get_player(self, user_id: str) -> Optional[dict]:
        """Get player profile."""
        return self.players.get(user_id)
    
    # Score operations
    def add_score(self, user_id: str, score: int, mode: GameMode) -> dict:
        """Add a score for a user."""
        player = self.players.get(user_id)
        if not player:
            raise ValueError("Player not found")
        
        # Update player stats
        player["games_played"] += 1
        is_new_high_score = score > player["high_score"]
        if is_new_high_score:
            player["high_score"] = score
        
        # Add score record
        score_record = {
            "user_id": user_id,
            "username": player["username"],
            "score": score,
            "mode": mode,
            "date": datetime.now(UTC),
        }
        self.scores.append(score_record)
        
        # Calculate rank
        rank = self.get_rank(score, mode)
        
        return {
            "is_new_high_score": is_new_high_score,
            "rank": rank,
        }
    
    def get_rank(self, score: int, mode: GameMode) -> int:
        """Calculate rank for a score."""
        mode_scores = [s["score"] for s in self.scores if s["mode"] == mode]
        mode_scores.sort(reverse=True)
        
        # Find position of score
        rank = 1
        for s in mode_scores:
            if score >= s:
                return rank
            rank += 1
        return rank
    
    def get_leaderboard(
        self,
        mode: Optional[GameMode] = None,
        limit: int = 10,
        offset: int = 0
    ) -> tuple[list[dict], int]:
        """Get leaderboard entries."""
        # Filter by mode if specified
        filtered_scores = self.scores
        if mode:
            filtered_scores = [s for s in self.scores if s["mode"] == mode]
        
        # Group by user, keep highest score
        user_best_scores: dict[str, dict] = {}
        for score in filtered_scores:
            user_id = score["user_id"]
            if user_id not in user_best_scores or score["score"] > user_best_scores[user_id]["score"]:
                user_best_scores[user_id] = score
        
        # Sort by score
        sorted_scores = sorted(user_best_scores.values(), key=lambda x: x["score"], reverse=True)
        
        # Add ranks
        entries = []
        for rank, score in enumerate(sorted_scores[offset:offset + limit], start=offset + 1):
            entries.append({
                "rank": rank,
                "username": score["username"],
                "score": score["score"],
                "date": score["date"],
            })
        
        return entries, len(sorted_scores)
    
    # Live game operations
    def get_live_games(
        self,
        mode: Optional[GameMode] = None,
        limit: int = 10
    ) -> list[dict]:
        """Get live games."""
        # Generate mock live games
        live_games = []
        
        # Take first 3 players
        player_ids = list(self.players.keys())[:3]
        for player_id in player_ids:
            player = self.players[player_id]
            game_state = self._generate_mock_game_state()
            
            live_game = {
                "id": str(uuid.uuid4()),
                "player": player,
                "game_state": game_state,
                "started_at": datetime.now(UTC) - timedelta(minutes=int(10 * (1 - game_state["score"] / 300))),
            }
            
            # Filter by mode if specified
            if mode is None or game_state["mode"] == mode:
                live_games.append(live_game)
        
        return live_games[:limit]
    
    def _generate_mock_game_state(self) -> dict:
        """Generate a mock game state."""
        import random
        
        score = random.randint(0, 200)
        snake_length = max(3, score // 10 + 3)
        
        body = [
            {"x": 15 - i, "y": 15}
            for i in range(snake_length)
        ]
        
        return {
            "snake": {
                "body": body,
                "direction": random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]),
            },
            "food": {
                "x": random.randint(0, 29),
                "y": random.randint(0, 29),
            },
            "score": score,
            "is_game_over": False,
            "is_paused": False,
            "mode": random.choice([GameMode.WALLS, GameMode.PASSTHROUGH]),
        }


# Global database instance
db = MockDatabase()
