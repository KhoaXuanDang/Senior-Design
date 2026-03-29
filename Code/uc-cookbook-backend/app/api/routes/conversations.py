from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.messaging import ConversationResponse, StartConversationRequest
from app.services.messaging_service import MessagingService


router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.post("", response_model=ConversationResponse)
async def start_conversation(
    payload: StartConversationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = MessagingService.start_conversation(db, current_user, payload.recipient_user_id)

    if payload.initial_message:
        MessagingService.send_message(db, conversation, current_user, payload.initial_message)

    return ConversationResponse.model_validate(conversation)


@router.get("", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversations = MessagingService.list_conversations(db, current_user)
    return [ConversationResponse.model_validate(conversation) for conversation in conversations]
