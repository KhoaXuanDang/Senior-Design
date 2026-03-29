from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.auth import AuthorResponse

ALLOWED_COMMENT_EMOJIS = frozenset({"👍", "❤️", "😂", "🔥"})


class AddCommentRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    parent_id: Optional[int] = Field(default=None, ge=1)


class SetReactionRequest(BaseModel):
    emoji: str = Field(..., min_length=1, max_length=16)


class ReactionSummary(BaseModel):
    emoji: str
    count: int
    reacted_by_me: bool = False


class RecipeCommentResponse(BaseModel):
    id: int
    recipe_id: int
    user_id: int
    parent_id: Optional[int] = None
    content: str
    created_at: datetime
    user: Optional[AuthorResponse] = None
    reactions: List[ReactionSummary] = []

    class Config:
        from_attributes = True
