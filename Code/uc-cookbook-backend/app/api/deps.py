from typing import Optional
from fastapi import Depends, HTTPException, status, Cookie, Header
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.core.security import decode_access_token


def _get_token_from_cookie_or_header(
    access_token: Optional[str] = Cookie(None),
    authorization: Optional[str] = Header(None),
) -> Optional[str]:
    """Get JWT from cookie (priority) or Authorization: Bearer header."""
    if access_token:
        return access_token
    if authorization and authorization.startswith("Bearer "):
        return authorization[7:].strip()
    return None


async def get_current_user(
    token: Optional[str] = Depends(_get_token_from_cookie_or_header),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from JWT cookie or Authorization header.
    
    Args:
        token: JWT from httpOnly cookie or Authorization: Bearer header
        db: Database session
        
    Returns:
        Current user object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    # Decode token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    # JWT "sub" can be int or string depending on library
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_user_optional(
    token: Optional[str] = Depends(_get_token_from_cookie_or_header),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency to optionally get the current user (doesn't fail if not authenticated).
    Useful for endpoints that work differently for authenticated vs anonymous users.
    
    Args:
        token: JWT from httpOnly cookie or Authorization: Bearer header
        db: Database session
        
    Returns:
        Current user object or None if not authenticated
    """
    if not token:
        return None
    
    payload = decode_access_token(token)
    if payload is None:
        return None
    
    user_id = payload.get("sub")
    if user_id is None:
        return None
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return None
    
    user = db.query(User).filter(User.id == user_id).first()
    return user
