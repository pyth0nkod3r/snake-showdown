"""
Integration test fixtures and configuration.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db_models import Base
from app.database import get_db


# Create in-memory SQLite database for integration testing
INTEGRATION_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    INTEGRATION_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
IntegrationSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def integration_db_session():
    """Create a fresh database session for each integration test."""
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create session
    session = IntegrationSessionLocal()

    yield session

    # Cleanup
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def integration_client(integration_db_session):
    """Create test client with database session override for integration tests."""

    def override_get_db():
        try:
            yield integration_db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers_integration(integration_client):
    """Create authenticated user and return auth headers for integration tests."""
    # Create a test user
    response = integration_client.post(
        "/api/auth/signup",
        json={
            "email": "integration@example.com",
            "password": "integrationpass123",
            "username": "integrationuser",
        },
    )
    assert response.status_code == 201

    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}
