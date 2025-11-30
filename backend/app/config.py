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
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # JWT Settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    model_config = ConfigDict(env_file=".env")


settings = Settings()
