"""
Authentication service - Business logic for user authentication.
"""
from typing import Optional
from app.database import db
from app.auth import create_access_token
from app.models import AuthUser, AuthResponse


class AuthService:
    """Service for authentication operations."""
    
    @staticmethod
    def signup(email: str, username: str, password: str) -> AuthResponse:
        """
        Register a new user.
        
        Raises:
            ValueError: If email or username already exists
        """
        # Create user in database
        user = db.create_user(email, username, password)
        
        # Generate JWT token
        token = create_access_token(data={"sub": user["id"]})
        
        # Prepare response
        auth_user = AuthUser(
            id=user["id"],
            username=user["username"],
            email=user["email"]
        )
        
        return AuthResponse(user=auth_user, token=token)
    
    @staticmethod
    def login(email: str, password: str) -> tuple[Optional[dict], Optional[str]]:
        """
        Authenticate a user.
        
        Returns:
            Tuple of (user_dict, error_message)
        """
        # Get user by email
        user = db.get_user_by_email(email)
        
        if not user:
            return None, "Invalid email or password"
        
        # Verify password
        if not db.verify_password(password, user["password_hash"]):
            return None, "Invalid email or password"
        
        return user, None
    
    @staticmethod
    def create_auth_response(user: dict) -> AuthResponse:
        """Create authentication response with token."""
        token = create_access_token(data={"sub": user["id"]})
        
        auth_user = AuthUser(
            id=user["id"],
            username=user["username"],
            email=user["email"]
        )
        
        return AuthResponse(user=auth_user, token=token)
    
    @staticmethod
    def get_user_info(user: dict) -> AuthUser:
        """Get user information."""
        return AuthUser(
            id=user["id"],
            username=user["username"],
            email=user["email"]
        )
