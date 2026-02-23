from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.db.models import CookbookSave, Recipe, User


class CookbookService:
    """Service layer for cookbook/save functionality"""
    
    @staticmethod
    def save_recipe(db: Session, recipe_id: int, user: User) -> CookbookSave:
        """
        Save a recipe to user's cookbook
        
        Args:
            db: Database session
            recipe_id: ID of recipe to save
            user: Current user
            
        Returns:
            CookbookSave object
            
        Raises:
            HTTPException: If recipe not found or already saved
        """
        # Check if recipe exists
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )
        
        # Check if already saved
        existing_save = db.query(CookbookSave).filter(
            CookbookSave.user_id == user.id,
            CookbookSave.recipe_id == recipe_id
        ).first()
        
        if existing_save:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Recipe already saved to cookbook"
            )
        
        # Create save
        cookbook_save = CookbookSave(
            user_id=user.id,
            recipe_id=recipe_id
        )
        
        try:
            db.add(cookbook_save)
            db.commit()
            db.refresh(cookbook_save)
            return cookbook_save
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Recipe already saved to cookbook"
            )
    
    @staticmethod
    def get_saved_recipes(db: Session, user: User) -> List[CookbookSave]:
        """
        Get all recipes saved by a user
        
        Args:
            db: Database session
            user: Current user
            
        Returns:
            List of CookbookSave objects with recipe data
        """
        saves = db.query(CookbookSave).filter(
            CookbookSave.user_id == user.id
        ).order_by(CookbookSave.created_at.desc()).all()
        
        return saves
    
    @staticmethod
    def remove_saved_recipe(db: Session, recipe_id: int, user: User) -> None:
        """
        Remove a recipe from user's cookbook
        
        Args:
            db: Database session
            recipe_id: ID of recipe to remove
            user: Current user
            
        Raises:
            HTTPException: If save not found
        """
        cookbook_save = db.query(CookbookSave).filter(
            CookbookSave.user_id == user.id,
            CookbookSave.recipe_id == recipe_id
        ).first()
        
        if not cookbook_save:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found in cookbook"
            )
        
        db.delete(cookbook_save)
        db.commit()
    
    @staticmethod
    def is_recipe_saved(db: Session, recipe_id: int, user_id: int) -> bool:
        """
        Check if a recipe is saved by a user
        
        Args:
            db: Database session
            recipe_id: Recipe ID
            user_id: User ID
            
        Returns:
            True if saved, False otherwise
        """
        save = db.query(CookbookSave).filter(
            CookbookSave.user_id == user_id,
            CookbookSave.recipe_id == recipe_id
        ).first()
        
        return save is not None
