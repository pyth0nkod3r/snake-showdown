"""
Integration tests for AuthService.
Tests authentication service with real database operations.
"""
import pytest
from app.services.auth_service import AuthService
from app.models import AuthResponse


def test_signup_success(integration_db_session):
    """Test successful user signup."""
    response = AuthService.signup(
        email="newuser@example.com",
        username="newuser",
        password="securepass123",
        db=integration_db_session
    )
    
    assert isinstance(response, AuthResponse)
    assert response.user.email == "newuser@example.com"
    assert response.user.username == "newuser"
    assert response.user.id is not None
    assert response.token is not None
    assert len(response.token) > 0


def test_signup_duplicate_email(integration_db_session):
    """Test signup with duplicate email raises error."""
    # Create first user
    AuthService.signup(
        email="duplicate@example.com",
        username="user1",
        password="pass123",
        db=integration_db_session
    )
    
    # Try to create second user with same email
    with pytest.raises(ValueError, match="Email already exists"):
        AuthService.signup(
            email="duplicate@example.com",
            username="user2",
            password="pass456",
            db=integration_db_session
        )


def test_signup_duplicate_username(integration_db_session):
    """Test signup with duplicate username raises error."""
    # Create first user
    AuthService.signup(
        email="user1@example.com",
        username="sameusername",
        password="pass123",
        db=integration_db_session
    )
    
    # Try to create second user with same username
    with pytest.raises(ValueError, match="Username already exists"):
        AuthService.signup(
            email="user2@example.com",
            username="sameusername",
            password="pass456",
            db=integration_db_session
        )


def test_login_success(integration_db_session):
    """Test successful login."""
    # Create user
    AuthService.signup(
        email="login@example.com",
        username="loginuser",
        password="correctpass",
        db=integration_db_session
    )
    
    # Login
    user, error = AuthService.login(
        email="login@example.com",
        password="correctpass",
        db=integration_db_session
    )
    
    assert user is not None
    assert error is None
    assert user["email"] == "login@example.com"
    assert user["username"] == "loginuser"


def test_login_wrong_password(integration_db_session):
    """Test login with incorrect password."""
    # Create user
    AuthService.signup(
        email="wrongpass@example.com",
        username="wrongpassuser",
        password="correctpass",
        db=integration_db_session
    )
    
    # Try to login with wrong password
    user, error = AuthService.login(
        email="wrongpass@example.com",
        password="wrongpassword",
        db=integration_db_session
    )
    
    assert user is None
    assert error == "Invalid email or password"


def test_login_nonexistent_email(integration_db_session):
    """Test login with non-existent email."""
    user, error = AuthService.login(
        email="nonexistent@example.com",
        password="somepass",
        db=integration_db_session
    )
    
    assert user is None
    assert error == "Invalid email or password"


def test_create_auth_response(integration_db_session):
    """Test creating auth response from user dict."""
    # Create user
    AuthService.signup(
        email="authresp@example.com",
        username="authrespuser",
        password="pass123",
        db=integration_db_session
    )
    
    # Login to get user dict
    user, _ = AuthService.login(
        email="authresp@example.com",
        password="pass123",
        db=integration_db_session
    )
    
    # Create auth response
    response = AuthService.create_auth_response(user)
    
    assert isinstance(response, AuthResponse)
    assert response.user.email == "authresp@example.com"
    assert response.token is not None


def test_get_user_info(integration_db_session):
    """Test getting user info from user dict."""
    # Create user
    AuthService.signup(
        email="userinfo@example.com",
        username="userinfouser",
        password="pass123",
        db=integration_db_session
    )
    
    # Login to get user dict
    user, _ = AuthService.login(
        email="userinfo@example.com",
        password="pass123",
        db=integration_db_session
    )
    
    # Get user info
    user_info = AuthService.get_user_info(user)
    
    assert user_info.email == "userinfo@example.com"
    assert user_info.username == "userinfouser"
    assert user_info.id == user["id"]


def test_complete_auth_flow(integration_db_session):
    """Test complete authentication flow: signup -> login -> get info."""
    # Signup
    signup_response = AuthService.signup(
        email="complete@example.com",
        username="completeuser",
        password="mypass123",
        db=integration_db_session
    )
    
    assert signup_response.user.email == "complete@example.com"
    signup_token = signup_response.token
    
    # Login
    user, error = AuthService.login(
        email="complete@example.com",
        password="mypass123",
        db=integration_db_session
    )
    
    assert user is not None
    assert error is None
    
    # Create new auth response
    login_response = AuthService.create_auth_response(user)
    
    assert login_response.user.email == "complete@example.com"
    assert login_response.user.username == "completeuser"
    
    # Both tokens should be valid (though different since generated at different times)
    assert len(signup_token) > 0
    assert len(login_response.token) > 0
