from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.auth import AuthorResponse


class StartConversationRequest(BaseModel):
    recipient_user_id: int = Field(..., ge=1)
    initial_message: Optional[str] = Field(default=None, min_length=1, max_length=4000)


class SendMessageRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000)


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    content: str
    created_at: datetime
    sender: Optional[AuthorResponse] = None

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    id: int
    user_one_id: int
    user_two_id: int
    user_one: Optional[AuthorResponse] = None
    user_two: Optional[AuthorResponse] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
