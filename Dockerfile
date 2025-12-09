# Unified Dockerfile for Snake Showdown (Backend + Frontend)
# Multi-stage build combining FastAPI backend with React frontend

# ============================================================================
# Stage 1: Build Frontend
# ============================================================================
FROM node:20-alpine as frontend-build

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm ci

# Copy frontend source code
COPY frontend/ ./

# Build the frontend for production
RUN npm run build

# ============================================================================
# Stage 2: Setup Backend
# ============================================================================
FROM python:3.12-slim as backend-base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Copy backend dependency files
COPY backend/pyproject.toml backend/uv.lock ./
COPY backend/README.md ./

# Install backend dependencies using uv
RUN uv sync --frozen --no-dev

# Copy backend application code
COPY backend/ ./

# ============================================================================
# Stage 3: Production Image with nginx + supervisor
# ============================================================================
FROM python:3.12-slim

# Install nginx, supervisor, curl, gettext (for envsubst), and psycopg2 dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
    curl \
    gettext-base \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy uv from backend-base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Copy Python dependencies and backend code from backend-base
COPY --from=backend-base /root/.cache/uv /root/.cache/uv
COPY --from=backend-base /app ./

# Copy frontend build from frontend-build stage
COPY --from=frontend-build /app/frontend/dist /usr/share/nginx/html

# Copy nginx configuration template
COPY nginx.conf.template /etc/nginx/conf.d/nginx.conf.template
RUN rm -f /etc/nginx/sites-enabled/default /etc/nginx/conf.d/default.conf

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create log directories
RUN mkdir -p /var/log/supervisor /var/log/nginx

# Expose port (will be set by Render via PORT env var)
EXPOSE ${PORT:-10000}

# Health check (uses PORT environment variable)
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-10000}/health || exit 1

# Run entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
