"""
Authentication route handlers.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.models import SignupRequest, LoginRequest, AuthResponse, AuthUser, ErrorResponse
from app.services.auth_service import AuthService
from app.auth import get_current_user
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    }
)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        return AuthService.signup(request.email, request.username, request.password, db)
    
    except ValueError as e:
        error_msg = str(e)
        if "Email already exists" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already in use"
            )
        elif "Username already exists" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already in use"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=AuthResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
    }
)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a user."""
    user, error = AuthService.login(request.email, request.password, db)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error
        )
    
    return AuthService.create_auth_response(user)


@router.post(
    "/logout",
    responses={
        200: {"description": "Successfully logged out"},
        401: {"model": ErrorResponse},
    }
)
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout user (invalidate token)."""
    return {"message": "Successfully logged out"}


@router.get(
    "/me",
    response_model=AuthUser,
    responses={
        401: {"model": ErrorResponse},
    }
)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user information."""
    return AuthService.get_user_info(current_user)
