from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
import enum
from app.db.session import Base


class DifficultyEnum(str, enum.Enum):
    """Recipe difficulty levels"""
    easy = "easy"
    medium = "medium"
    hard = "hard"


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
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = relationship("User", back_populates="recipes")
    cookbook_saves = relationship("CookbookSave", back_populates="recipe", cascade="all, delete-orphan")


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
