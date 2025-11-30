# Snake Showdown Backend API

FastAPI backend implementation for the Snake Showdown game, built according to the OpenAPI specification.

## Features

✅ **Authentication** - JWT-based user authentication with signup, login, logout  
✅ **Game Management** - Score submission, leaderboards, live game spectating  
✅ **Player Profiles** - Player statistics and game history  
✅ **Mock Database** - In-memory database for development (easily replaceable)  
✅ **Comprehensive Tests** - 32 tests covering all endpoints  
✅ **CORS Support** - Configured for frontend integration

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── models.py            # Pydantic data models
│   ├── database.py          # Mock database implementation
│   ├── auth.py              # JWT authentication utilities
│   └── routes/
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       ├── game.py          # Game endpoints
│       └── player.py        # Player endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures
│   ├── test_auth.py         # Auth endpoint tests
│   ├── test_game.py         # Game endpoint tests
│   ├── test_player.py       # Player endpoint tests
│   └── test_main.py         # Main app tests
├── main.py                  # Application runner
└── pyproject.toml           # Dependencies (uv)
```

## Setup

### Prerequisites

- Python 3.12+
- `uv` package manager

### Installation

```bash
cd backend

# Sync dependencies from lockfile
uv sync

# Or manually add packages
uv add fastapi uvicorn pydantic
```

## Running the Server

### Quick Start

From the backend directory:

```bash
cd backend
uv run python main.py
```

The server will start on **http://localhost:3000** with auto-reload enabled.

### Alternative: Using Uvicorn Directly

```bash
# Basic
uv run uvicorn app.main:app --reload --port 3000

# With all options
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 3000
```

**Options:**
- `--reload` - Auto-restart on code changes (development only)
- `--host 0.0.0.0` - Accept connections from any IP
- `--port 3000` - Specify port (default: 3000)

### Access Points

Once running, the API is available at:

- **API Base URL**: http://localhost:3000
- **Interactive API Docs (Swagger UI)**: http://localhost:3000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:3000/redoc
- **Health Check**: http://localhost:3000/health

### Test the Server

```bash
# In another terminal
curl http://localhost:3000/health
# Should return: {"status":"healthy"}

# Test signup
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","username":"testuser"}'
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=app --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_auth.py

# Run specific test
uv run pytest tests/test_auth.py::test_signup_success
```

## API Endpoints

### Authentication (`/api/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/signup` | Register new user | No |
| POST | `/api/auth/login` | Authenticate user | No |
| POST | `/api/auth/logout` | Logout current user | Yes |
| GET | `/api/auth/me` | Get current user info | Yes |

### Game (`/api/game`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/game/score` | Submit game score | Yes |
| GET | `/api/game/leaderboard` | Get rankings | No |
| GET | `/api/game/live` | Get active games | No |

### Player (`/api/player`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/player/profile` | Get player profile | Yes |

## Example Usage

### Signup

```bash
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "player@example.com",
    "password": "securepass123",
    "username": "coolplayer"
  }'
```

### Login

```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "player@example.com",
    "password": "securepass123"
  }'
```

### Submit Score (requires token)

```bash
curl -X POST http://localhost:3000/api/game/score \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "score": 250,
    "mode": "walls"
  }'
```

### Get Leaderboard

```bash
curl http://localhost:3000/api/game/leaderboard?mode=walls&limit=10
```

## Configuration

Edit `app/config.py` or create a `.env` file:

```env
# CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# JWT settings
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# API settings
API_TITLE=Snake Showdown API
API_VERSION=1.0.0
```

## Database

The current implementation uses an in-memory mock database (`app/database.py`). To replace with a real database:

1. Install database driver (e.g., `uv add sqlalchemy asyncpg`)
2. Create database models in `app/db_models.py`
3. Replace `MockDatabase` class with real database connection
4. Update route handlers to use new database

Mock data includes 5 pre-populated players with scores for testing.

## Testing Details

**Test Coverage**: 32 tests covering:
- ✅ User registration (valid, duplicate email, duplicate username)
- ✅ User login (success, wrong password, non-existent user)
- ✅ JWT authentication (valid token, invalid token, missing token)
- ✅ Score submission (valid, invalid mode, negative scores)
- ✅ Leaderboard queries (all modes, filtering, pagination)
- ✅ Live games (retrieval, filtering)
- ✅ Player profiles (retrieval, updates after score submission)

## CORS Configuration

The API is pre-configured to accept requests from:
- `http://localhost:5173` (Vite default)
- `http://localhost:3000` (alternative frontend)

Update `app/config.py` to add more origins.

## Next Steps

1. **Replace Mock Database** - Integrate PostgreSQL or MongoDB
2. **Add WebSockets** - Real-time game state updates for spectating
3. **Email Verification** - Add email verification for signups
4. **Rate Limiting** - Prevent abuse with rate limiting middleware
5. **Logging** - Add structured logging
6. **Docker** - Create Dockerfile for deployment
7. **CI/CD** - Set up automated testing and deployment

## Troubleshooting

### Port Already in Use

```bash
# Find and kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use a different port
uv run uvicorn app.main:app --reload --port 8000
```

### Dependencies Not Found

```bash
# Re-sync dependencies
uv sync

# Or clear cache and reinstall
rm -rf .venv
uv sync
```

## License

See main project LICENSE file.
