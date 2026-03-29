from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.auth import AuthorResponse
from app.db.models import DifficultyEnum, VisibilityEnum


class RecipeBase(BaseModel):
    """Base recipe schema"""
    title: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=1)
    ingredients: List[str] = Field(..., min_items=1)
    steps: List[str] = Field(..., min_items=1)
    tags: List[str] = Field(default_factory=list, max_items=10)
    time_minutes: int = Field(..., ge=1)
    difficulty: DifficultyEnum
    image_url: Optional[str] = Field(None, max_length=500)
    is_published: bool = False
    visibility: VisibilityEnum = VisibilityEnum.public


class CreateRecipeRequest(RecipeBase):
    """Schema for creating a recipe"""
    pass


class UpdateRecipeRequest(BaseModel):
    """Schema for updating a recipe (all fields optional)"""
    title: Optional[str] = Field(None, min_length=3, max_length=120)
    description: Optional[str] = None
    ingredients: Optional[List[str]] = None
    steps: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    time_minutes: Optional[int] = Field(None, ge=1)
    difficulty: Optional[DifficultyEnum] = None
    image_url: Optional[str] = None
    is_published: Optional[bool] = None
    visibility: Optional[VisibilityEnum] = None


class RecipeResponse(RecipeBase):
    """Schema for recipe in responses"""
    id: int
    author_id: int
    author: Optional[AuthorResponse] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class RecipesResponse(BaseModel):
    """Schema for paginated recipe list"""
    recipes: List[RecipeResponse]
    total: int
    limit: int
    offset: int


# Backward-compatible aliases used in existing code
RecipeCreate = CreateRecipeRequest
RecipeUpdate = UpdateRecipeRequest
