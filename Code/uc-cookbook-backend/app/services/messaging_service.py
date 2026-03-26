from typing import List, Tuple
from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.db.models import Conversation, Message, User


class MessagingService:
    @staticmethod
    def _normalized_pair(user_id_a: int, user_id_b: int) -> Tuple[int, int]:
        return (user_id_a, user_id_b) if user_id_a < user_id_b else (user_id_b, user_id_a)

    @staticmethod
    def get_conversation_between_users(db: Session, user_id_a: int, user_id_b: int) -> Conversation | None:
        low_id, high_id = MessagingService._normalized_pair(user_id_a, user_id_b)
        return db.query(Conversation).filter(
            Conversation.user_one_id == low_id,
            Conversation.user_two_id == high_id,
        ).first()

    @staticmethod
    def start_conversation(db: Session, current_user: User, recipient_user_id: int) -> Conversation:
        if recipient_user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot start a conversation with yourself",
            )

        recipient = db.query(User).filter(User.id == recipient_user_id).first()
        if not recipient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipient not found",
            )

        existing = MessagingService.get_conversation_between_users(db, current_user.id, recipient_user_id)
        if existing:
            return existing

        low_id, high_id = MessagingService._normalized_pair(current_user.id, recipient_user_id)
        conversation = Conversation(user_one_id=low_id, user_two_id=high_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    @staticmethod
    def list_conversations(db: Session, user: User) -> List[Conversation]:
        return db.query(Conversation).filter(
            or_(
                Conversation.user_one_id == user.id,
                Conversation.user_two_id == user.id,
            )
        ).order_by(Conversation.updated_at.desc(), Conversation.created_at.desc()).all()

    @staticmethod
    def get_conversation(db: Session, conversation_id: int) -> Conversation:
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )
        return conversation

    @staticmethod
    def list_messages(db: Session, conversation_id: int) -> List[Message]:
        return db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).all()

    @staticmethod
    def send_message(db: Session, conversation: Conversation, sender: User, content: str) -> Message:
        message = Message(
            conversation_id=conversation.id,
            sender_id=sender.id,
            content=content,
        )
        db.add(message)
        db.commit()
        db.refresh(message)

        conversation.updated_at = message.created_at
        db.commit()

        return message
