#!/bin/bash
set -e

# Set default PORT if not provided (for local development)
export PORT=${PORT:-10000}

# Generate nginx config from template with PORT substitution
echo "Configuring nginx to listen on port $PORT..."
envsubst '${PORT}' < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/default.conf

# Wait for PostgreSQL to be ready (with timeout)
if [ -n "$DATABASE_URL" ]; then
  echo "Waiting for PostgreSQL..."
  timeout=30
  elapsed=0
  until uv run python -c "
import sys
import os
from sqlalchemy import create_engine
try:
    engine = create_engine(os.environ['DATABASE_URL'])
    conn = engine.connect()
    conn.close()
    sys.exit(0)
except Exception as e:
    sys.exit(1)
" 2>/dev/null; do
    if [ $elapsed -ge $timeout ]; then
      echo "⚠️  PostgreSQL connection timeout - continuing anyway..."
      break
    fi
    sleep 1
    elapsed=$((elapsed + 1))
  done
  echo "PostgreSQL is ready!"
fi

# Initialize database tables
echo "Initializing database..."
uv run python -c "from app.database import init_db; init_db()"

# Seed database if SEED_DB environment variable is set
if [ "$SEED_DB" = "true" ]; then
  echo "Seeding database with demo data..."
  uv run python -c "from app.database import seed_db; seed_db()"
fi

# Start supervisor to manage both nginx and backend
echo "Starting services with supervisor..."
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
