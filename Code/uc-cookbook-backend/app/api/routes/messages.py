from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.messaging import MessageResponse, SendMessageRequest
from app.services.authorization_service import is_participant
from app.services.messaging_service import MessagingService


router = APIRouter(prefix="/conversations", tags=["Messages"])


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = MessagingService.get_conversation(db, conversation_id)
    if not is_participant(conversation, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this conversation")

    messages = MessagingService.list_messages(db, conversation_id)
    return [MessageResponse.model_validate(message) for message in messages]


@router.post("/{conversation_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    conversation_id: int,
    payload: SendMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = MessagingService.get_conversation(db, conversation_id)
    if not is_participant(conversation, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this conversation")

    message = MessagingService.send_message(db, conversation, current_user, payload.content)
    return MessageResponse.model_validate(message)
