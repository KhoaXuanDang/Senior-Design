from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.auth import AuthorResponse


class AddCommentRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)


class RecipeCommentResponse(BaseModel):
    id: int
    recipe_id: int
    user_id: int
    content: str
    created_at: datetime
    user: Optional[AuthorResponse] = None

    class Config:
        from_attributes = True
