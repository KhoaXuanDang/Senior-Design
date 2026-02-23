from typing import Optional
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str
    message: Optional[str] = None


class SuccessResponse(BaseModel):
    """Standard success response"""
    message: str
