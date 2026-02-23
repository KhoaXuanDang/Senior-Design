from datetime import datetime
from pydantic import BaseModel
from app.schemas.recipe import RecipeResponse


class CookbookSaveResponse(BaseModel):
    """Schema for cookbook save entry"""
    id: int
    user_id: int
    recipe_id: int
    recipe: RecipeResponse
    saved_at: datetime
    
    class Config:
        from_attributes = True
        # Map created_at to saved_at for frontend compatibility
        populate_by_name = True
    
    @classmethod
    def from_orm(cls, obj):
        """Custom ORM mapping to handle saved_at"""
        data = {
            'id': obj.id,
            'user_id': obj.user_id,
            'recipe_id': obj.recipe_id,
            'recipe': obj.recipe,
            'saved_at': obj.created_at  # Map created_at to saved_at
        }
        return cls(**data)
