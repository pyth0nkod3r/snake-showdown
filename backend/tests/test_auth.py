"""
Tests for authentication endpoints.
"""
import pytest


def test_signup_success(client):
    """Test successful user signup."""
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "newuser@example.com",
            "password": "password123",
            "username": "newuser"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "user" in data
    assert "token" in data
    assert data["user"]["email"] == "newuser@example.com"
    assert data["user"]["username"] == "newuser"
    assert "id" in data["user"]


def test_signup_duplicate_email(client):
    """Test signup with duplicate email."""
    # First signup
    client.post(
        "/api/auth/signup",
        json={
            "email": "duplicate@example.com",
            "password": "password123",
            "username": "user1"
        }
    )
    
    # Second signup with same email
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "duplicate@example.com",
            "password": "password123",
            "username": "user2"
        }
    )
    
    assert response.status_code == 409


def test_signup_duplicate_username(client):
    """Test signup with duplicate username."""
    # First signup
    client.post(
        "/api/auth/signup",
        json={
            "email": "user1@example.com",
            "password": "password123",
            "username": "sameusername"
        }
    )
    
    # Second signup with same username
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "user2@example.com",
            "password": "password123",
            "username": "sameusername"
        }
    )
    
    assert response.status_code == 409


def test_signup_invalid_email(client):
    """Test signup with invalid email."""
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "notanemail",
            "password": "password123",
            "username": "testuser"
        }
    )
    
    assert response.status_code == 422


def test_signup_short_password(client):
    """Test signup with password too short."""
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "test@example.com",
            "password": "short",
            "username": "testuser"
        }
    )
    
    assert response.status_code == 422


def test_login_success(client):
    """Test successful login."""
    # First create a user
    client.post(
        "/api/auth/signup",
        json={
            "email": "login@example.com",
            "password": "password123",
            "username": "loginuser"
        }
    )
    
    # Then login
    response = client.post(
        "/api/auth/login",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert "token" in data
    assert data["user"]["email"] == "login@example.com"


def test_login_wrong_password(client):
    """Test login with wrong password."""
    # Create a user
    client.post(
        "/api/auth/signup",
        json={
            "email": "user@example.com",
            "password": "correctpassword",
            "username": "testuser"
        }
    )
    
    # Try to login with wrong password
    response = client.post(
        "/api/auth/login",
        json={
            "email": "user@example.com",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    """Test login with non-existent user."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 401


def test_get_me_success(client, auth_headers):
    """Test getting current user."""
    response = client.get("/api/auth/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"


def test_get_me_unauthorized(client):
    """Test getting current user without authentication."""
    response = client.get("/api/auth/me")
    
    assert response.status_code == 401


def test_get_me_invalid_token(client):
    """Test getting current user with invalid token."""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    
    assert response.status_code == 401


def test_logout_success(client, auth_headers):
    """Test successful logout."""
    response = client.post("/api/auth/logout", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_logout_unauthorized(client):
    """Test logout without authentication."""
    response = client.post("/api/auth/logout")
    
    assert response.status_code == 401
