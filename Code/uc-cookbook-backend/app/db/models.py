from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    JSON,
    Enum as SQLEnum,
    UniqueConstraint,
    Boolean,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
import enum
from app.db.session import Base


class DifficultyEnum(str, enum.Enum):
    """Recipe difficulty levels"""
    easy = "easy"
    medium = "medium"
    hard = "hard"


class VisibilityEnum(str, enum.Enum):
    """Recipe visibility levels"""
    public = "public"
    private = "private"


class User(Base):
    """User model for authentication and recipe authorship"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    recipes = relationship("Recipe", back_populates="author", cascade="all, delete-orphan")
    cookbook_saves = relationship("CookbookSave", back_populates="user", cascade="all, delete-orphan")
    recipe_comments = relationship("RecipeComment", back_populates="user", cascade="all, delete-orphan")
    conversations_as_user_one = relationship(
        "Conversation",
        foreign_keys="Conversation.user_one_id",
        back_populates="user_one",
        cascade="all, delete-orphan",
    )
    conversations_as_user_two = relationship(
        "Conversation",
        foreign_keys="Conversation.user_two_id",
        back_populates="user_two",
        cascade="all, delete-orphan",
    )
    sent_messages = relationship("Message", back_populates="sender", cascade="all, delete-orphan")


class Recipe(Base):
    """Recipe model containing cooking instructions and metadata"""
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False, index=True)
    description = Column(Text, nullable=False)
    ingredients = Column(JSON, nullable=False)  # List of strings
    steps = Column(JSON, nullable=False)  # List of strings
    tags = Column(JSON, nullable=False, default=list)  # List of strings
    time_minutes = Column(Integer, nullable=False)
    difficulty = Column(SQLEnum(DifficultyEnum), nullable=False)
    image_url = Column(String(500), nullable=True)
    is_published = Column(Boolean, nullable=False, default=False)
    visibility = Column(SQLEnum(VisibilityEnum), nullable=False, default=VisibilityEnum.public)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = relationship("User", back_populates="recipes")
    cookbook_saves = relationship("CookbookSave", back_populates="recipe", cascade="all, delete-orphan")
    comments = relationship("RecipeComment", back_populates="recipe", cascade="all, delete-orphan")


class CookbookSave(Base):
    """Junction table for users saving recipes to their cookbook"""
    __tablename__ = "cookbook_saves"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="cookbook_saves")
    recipe = relationship("Recipe", back_populates="cookbook_saves")
    
    # Unique constraint to prevent duplicate saves
    __table_args__ = (
        UniqueConstraint('user_id', 'recipe_id', name='unique_user_recipe'),
    )


class RecipeComment(Base):
    """Comments made by users on recipes"""
    __tablename__ = "recipe_comments"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    recipe = relationship("Recipe", back_populates="comments")
    user = relationship("User", back_populates="recipe_comments")


class Conversation(Base):
    """Direct conversation between two users"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_one_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_two_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_one = relationship("User", foreign_keys=[user_one_id], back_populates="conversations_as_user_one")
    user_two = relationship("User", foreign_keys=[user_two_id], back_populates="conversations_as_user_two")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("user_one_id", "user_two_id", name="unique_conversation_pair"),
        CheckConstraint("user_one_id < user_two_id", name="check_user_order"),
    )


class Message(Base):
    """Message sent inside a conversation"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("User", back_populates="sent_messages")
