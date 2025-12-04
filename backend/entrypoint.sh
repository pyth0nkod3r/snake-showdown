#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
until uv run python -c "
import sys
import psycopg2
try:
    psycopg2.connect(
        host='$DB_HOST',
        port='$DB_PORT',
        user='postgres',
        password='postgres123',
        dbname='snake_showdown',
        connect_timeout=3
    ).close()
    sys.exit(0)
except Exception:
    sys.exit(1)
" 2>/dev/null; do
  sleep 0.5
done
echo "PostgreSQL is ready!"

# Initialize database tables
echo "Initializing database..."
uv run python -c "from app.database import init_db; init_db()"

# Seed database if SEED_DB environment variable is set
if [ "$SEED_DB" = "true" ]; then
  echo "Seeding database with demo data..."
  uv run python -c "from app.database import seed_db; seed_db()"
fi

# Start the application
echo "Starting FastAPI server..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 3000
