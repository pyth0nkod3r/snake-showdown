.PHONY: help install dev test test-cov lint format clean db-init db-migrate db-reset

# Default target
help:
	@echo "Snake Showdown Backend - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install    - Install dependencies from lockfile"
	@echo "  make dev        - Start development server with auto-reload"
	@echo "  make test       - Run tests"
	@echo "  make test-cov   - Run tests with coverage report"
	@echo "  make lint       - Run linting checks"
	@echo "  make format     - Format code"
	@echo ""
	@echo "Database:"
	@echo "  make db-init    - Initialize database"
	@echo "  make db-migrate - Run database migrations"
	@echo "  make db-reset   - Reset database (WARNING: destroys data)"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean      - Remove cache and temporary files"

# Install dependencies
install:
	uv sync

# Start development server
dev:
	uv run uvicorn app.main:app --reload --port 3000

# Run tests
test:
	uv run pytest

# Run tests with coverage
test-cov:
	uv run pytest --cov=app --cov-report=html --cov-report=term

# Run integration tests
test-integration:
	uv run pytest tests_integration

# Run all tests (unit + integration)
test-all:
	uv run pytest tests tests_integration

# Run integration tests with coverage
test-integration-cov:
	uv run pytest tests_integration --cov=app --cov-report=html --cov-report=term

# Lint code
lint:
	uv run ruff check app tests

# Format code
format:
	uv run ruff format app tests

# Database initialization
db-init:
	uv run python app/init_db.py --seed

# Database migrations (if using alembic)
db-migrate:
	uv run alembic upgrade head

# Reset database (WARNING: destroys all data)
db-reset:
	@echo "Are you sure you want to reset the database? This will destroy all data!"
	@read -p "Type 'yes' to confirm: " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		rm -f snake_showdown.db; \
		uv run python app/init_db.py --seed; \
		echo "Database reset complete"; \
	else \
		echo "Database reset cancelled"; \
	fi

# Clean up cache and temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf htmlcov .coverage
	@echo "Cache and temporary files removed"
