from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.api.deps import get_current_user
from app.schemas.auth import UserCreate, UserLogin, AuthResponse, UserResponse
from app.schemas.common import SuccessResponse
from app.services.auth_service import AuthService
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    Args:
        user_data: User registration data (email, username, password)
        response: FastAPI response object for setting cookies
        db: Database session
        
    Returns:
        AuthResponse with user data and token in cookie
    """
    # Create user
    user = AuthService.register_user(db, user_data)
    
    # Create token
    token = AuthService.create_user_token(user)
    
    # Set httpOnly cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        path="/",  # Make cookie available for all routes
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return AuthResponse(
        user=UserResponse.model_validate(user),
        message="User registered successfully",
        access_token=token,  # Also return in body for frontend compatibility
        token=token
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    credentials: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Login user with email and password
    
    Args:
        credentials: Login credentials (email, password)
        response: FastAPI response object for setting cookies
        db: Database session
        
    Returns:
        AuthResponse with user data and token in cookie
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Authenticate user
    user = AuthService.authenticate_user(db, credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create token
    token = AuthService.create_user_token(user)
    
    # Set httpOnly cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        path="/",  # Make cookie available for all routes
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return AuthResponse(
        user=UserResponse.model_validate(user),
        message="Login successful",
        access_token=token,  # Also return in body for frontend compatibility
        token=token
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information
    
    Args:
        current_user: Authenticated user (from JWT cookie)
        
    Returns:
        Current user information
        
    Raises:
        HTTPException: If not authenticated
    """
    return UserResponse.model_validate(current_user)


@router.post("/logout", response_model=SuccessResponse)
async def logout(response: Response):
    """
    Logout user by clearing the authentication cookie
    
    Args:
        response: FastAPI response object for clearing cookies
        
    Returns:
        Success message
    """
    response.delete_cookie(key="access_token", path="/")
    
    return SuccessResponse(message="Logout successful")
