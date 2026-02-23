from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.api.deps import get_current_user
from app.schemas.cookbook import CookbookSaveResponse
from app.schemas.common import SuccessResponse
from app.services.cookbook_service import CookbookService

router = APIRouter(prefix="/cookbook", tags=["Cookbook"])


@router.get("", response_model=List[CookbookSaveResponse])
async def get_cookbook(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all recipes saved to user's cookbook (authentication required)
    
    Args:
        current_user: Authenticated user (from JWT cookie)
        db: Database session
        
    Returns:
        List of saved recipes with full recipe data
    """
    saves = CookbookService.get_saved_recipes(db, current_user)
    return [CookbookSaveResponse.from_orm(save) for save in saves]


@router.post("/{recipe_id}", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def save_recipe(
    recipe_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Save a recipe to user's cookbook (authentication required)
    
    Args:
        recipe_id: ID of recipe to save
        current_user: Authenticated user (from JWT cookie)
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If recipe not found or already saved
    """
    CookbookService.save_recipe(db, recipe_id, current_user)
    return SuccessResponse(message="Recipe saved to cookbook")


@router.delete("/{recipe_id}", response_model=SuccessResponse)
async def remove_recipe(
    recipe_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a recipe from user's cookbook (authentication required)
    
    Args:
        recipe_id: ID of recipe to remove
        current_user: Authenticated user (from JWT cookie)
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If recipe not found in cookbook
    """
    CookbookService.remove_saved_recipe(db, recipe_id, current_user)
    return SuccessResponse(message="Recipe removed from cookbook")
