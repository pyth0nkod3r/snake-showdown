# Snake Showdown 🐍

<!-- CI/CD Pipeline Active -->

A modern, full-stack Snake game with real-time leaderboards and spectating features.

## Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.12+
- **uv** package manager for Python

### Running Both Servers

From the root directory:

```bash
# Install dependencies
npm install

# Run both frontend and backend together
npm run dev
```

This will start:

- **Frontend** on http://localhost:5173 (green output)
- **Backend** on http://localhost:3000 (blue output)

### Running Individually

**Backend only:**

```bash
cd backend
make dev
# or: uv run uvicorn app.main:app --reload --port 3000
```

**Frontend only:**

```bash
cd frontend
npm run dev
```

### Demo Login Credentials

The app comes pre-loaded with demo users for testing. You can log in with any of these credentials:

**Email:** Any of the following:

- `snake@example.com`
- `neon@example.com`
- `grid@example.com`
- `arcade@example.com`
- `pixel@example.com`
- (and more - see backend code for full list)

**Password:** `demo123` (for all demo users)

Or create your own account using the signup form!

## Project Structure

```
snake-showdown/
├── frontend/          # React + TypeScript + Vite
│   ├── src/
│   │   ├── pages/     # Game, Auth, Leaderboard, Spectate
│   │   ├── components/
│   │   ├── services/  # API integration
│   │   └── hooks/     # Snake game logic
│   └── package.json
├── backend/           # FastAPI + Python
│   ├── app/
│   │   ├── routes/    # API endpoints
│   │   ├── services/  # Business logic
│   │   └── models.py  # Pydantic schemas
│   ├── tests/
│   ├── Makefile       # Backend commands
│   └── pyproject.toml
└── package.json       # Root scripts with concurrently
```

## Available Commands

### Root Level

```bash
npm run dev              # Run both servers concurrently
npm run dev:frontend     # Run frontend only
npm run dev:backend      # Run backend only
npm run test             # Run all tests
npm run test:frontend    # Run frontend tests
npm run test:backend     # Run backend tests
```

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment:

- ✅ **Automated Testing**: Backend unit tests, backend integration tests, and frontend tests run on every push to main
- ✅ **Conditional Deployment**: Deployment to Render only happens if all tests pass
- ✅ **Parallel Execution**: Tests run concurrently for faster feedback

### Pipeline Workflow

1. **Push to main** → Triggers CI/CD pipeline
2. **Test Jobs Run** (in parallel):
   - Backend unit tests with pytest
   - Backend integration tests with pytest
   - Frontend tests with Vitest
3. **If all tests pass** → Deploy to Render
4. **If any test fails** → Deployment blocked

View pipeline status in the **Actions** tab on GitHub.

**Setup:** See [.github/RENDER_DEPLOY_SETUP.md](.github/RENDER_DEPLOY_SETUP.md) for deployment configuration.

### Backend (from `/backend`)

```bash
make dev        # Start dev server
make test       # Run tests
make test-cov   # Tests with coverage
make lint       # Lint code
make format     # Format code
make clean      # Clean cache
make db-init    # Initialize database
make db-reset   # Reset database
```

### Frontend (from `/frontend`)

```bash
npm run dev       # Start dev server
npm run build     # Build for production
npm run test      # Run tests
npm run test:ui   # Tests with UI
npm run lint      # Lint code
```

## Features

✅ **Multiplayer Snake Game** - Classic snake with walls/passthrough modes  
✅ **Real-time Leaderboards** - Compete for high scores  
✅ **JWT Authentication** - Secure user accounts  
✅ **Live Game Spectating** - Watch others play  
✅ **Player Profiles** - Track stats and history  
✅ **Responsive Design** - Works on desktop and mobile  
✅ **Comprehensive Tests** - Both frontend and backend tested

## Tech Stack

**Frontend:**

- React 18 + TypeScript
- Vite (build tool)
- TailwindCSS + shadcn/ui
- Vitest (testing)

**Backend:**

- FastAPI (Python)
- JWT authentication
- Pydantic validation
- Pytest (testing)

## API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:3000/docs
- **ReDoc**: http://localhost:3000/redoc

## Development

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend connects to the backend API at `http://localhost:3000/api`.

### Backend Setup

```bash
cd backend
uv sync
make dev
```

See [backend/README.md](backend/README.md) for detailed backend documentation.

## Testing

Run all tests:

```bash
npm test
```

Or individually:

```bash
# Backend tests (from /backend)
make test

# Frontend tests (from /frontend)
npm test
```

## Contributing

1. Make changes to your feature branch
2. Run tests: `npm test`
3. Commit with conventional commits
4. Push and create a pull request

## License

MIT License - see LICENSE file for details
