from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user data in responses"""
    id: int
    email: str
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class AuthorResponse(BaseModel):
    """Minimal author info for recipe responses"""
    id: int
    username: str
    
    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Schema for authentication responses"""
    user: UserResponse
    message: Optional[str] = None
    
    # Frontend expects these fields (even though we use cookies)
    access_token: Optional[str] = None
    token: Optional[str] = None
