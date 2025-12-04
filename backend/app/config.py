"""
Configuration settings for the Snake Showdown API.
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    api_title: str = "Snake Showdown API"
    api_version: str = "1.0.0"
    api_description: str = "Backend API for Snake Showdown game"

    # CORS Settings
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080",
    ]

    # JWT Settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours

    # Database Settings
    database_url: str = (
        "postgresql://postgres:postgres123@localhost:5432/snake_showdown"
    )
    database_echo: bool = False  # Set to True for SQL query logging

    # Connection pool settings (for PostgreSQL)
    database_pool_size: int = 5
    database_max_overflow: int = 10

    model_config = ConfigDict(env_file=".env")


settings = Settings()
