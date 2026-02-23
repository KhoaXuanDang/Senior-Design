from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from fastapi import HTTPException, status
from app.db.models import Recipe, User
from app.schemas.recipe import RecipeCreate, RecipeUpdate


class RecipeService:
    """Service layer for recipe business logic"""
    
    @staticmethod
    def create_recipe(db: Session, recipe_data: RecipeCreate, user: User) -> Recipe:
        """
        Create a new recipe
        
        Args:
            db: Database session
            recipe_data: Recipe creation data
            user: Author user
            
        Returns:
            Created recipe object
        """
        db_recipe = Recipe(
            title=recipe_data.title,
            description=recipe_data.description,
            ingredients=recipe_data.ingredients,
            steps=recipe_data.steps,
            tags=recipe_data.tags,
            time_minutes=recipe_data.time_minutes,
            difficulty=recipe_data.difficulty,
            image_url=recipe_data.image_url,
            author_id=user.id
        )
        
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        return db_recipe
    
    @staticmethod
    def get_recipe_by_id(db: Session, recipe_id: int) -> Optional[Recipe]:
        """
        Get a recipe by ID
        
        Args:
            db: Database session
            recipe_id: Recipe ID
            
        Returns:
            Recipe object or None if not found
        """
        return db.query(Recipe).filter(Recipe.id == recipe_id).first()
    
    @staticmethod
    def get_recipes(
        db: Session,
        search: Optional[str] = None,
        tag: Optional[str] = None,
        difficulty: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[List[Recipe], int]:
        """
        Get recipes with filtering and pagination
        
        Args:
            db: Database session
            search: Search query for title/description
            tag: Filter by tag
            difficulty: Filter by difficulty
            limit: Max number of results
            offset: Number of results to skip
            
        Returns:
            Tuple of (list of recipes, total count)
        """
        query = db.query(Recipe)
        
        # Apply filters
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Recipe.title.ilike(search_filter),
                    Recipe.description.ilike(search_filter)
                )
            )
        
        if tag:
            # SQLite JSON filtering
            query = query.filter(Recipe.tags.contains(tag))
        
        if difficulty:
            query = query.filter(Recipe.difficulty == difficulty)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and order
        recipes = query.order_by(Recipe.created_at.desc()).limit(limit).offset(offset).all()
        
        return recipes, total
    
    @staticmethod
    def update_recipe(
        db: Session,
        recipe: Recipe,
        recipe_data: RecipeUpdate,
        user: User
    ) -> Recipe:
        """
        Update a recipe
        
        Args:
            db: Database session
            recipe: Recipe to update
            recipe_data: Update data
            user: User attempting update
            
        Returns:
            Updated recipe object
            
        Raises:
            HTTPException: If user is not the author
        """
        # Verify ownership
        if recipe.author_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this recipe"
            )
        
        # Update fields
        update_data = recipe_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(recipe, field, value)
        
        db.commit()
        db.refresh(recipe)
        return recipe
    
    @staticmethod
    def delete_recipe(db: Session, recipe: Recipe, user: User) -> None:
        """
        Delete a recipe
        
        Args:
            db: Database session
            recipe: Recipe to delete
            user: User attempting deletion
            
        Raises:
            HTTPException: If user is not the author
        """
        # Verify ownership
        if recipe.author_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this recipe"
            )
        
        db.delete(recipe)
        db.commit()
