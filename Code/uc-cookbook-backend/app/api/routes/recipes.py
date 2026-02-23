from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.api.deps import get_current_user
from app.schemas.recipe import RecipeCreate, RecipeResponse, RecipesResponse
from app.services.recipe_service import RecipeService

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get("", response_model=RecipesResponse)
async def get_recipes(
    search: Optional[str] = Query(None, description="Search in title and description"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty (easy/medium/hard)"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of recipes with optional filtering
    
    Query Parameters:
        - search: Search term for title/description
        - tag: Filter by specific tag
        - difficulty: Filter by difficulty level
        - limit: Max results (1-100, default 20)
        - offset: Skip N results (for pagination)
        
    Returns:
        Paginated list of recipes with total count
    """
    recipes, total = RecipeService.get_recipes(
        db=db,
        search=search,
        tag=tag,
        difficulty=difficulty,
        limit=limit,
        offset=offset
    )
    
    return RecipesResponse(
        recipes=[RecipeResponse.model_validate(r) for r in recipes],
        total=total,
        limit=limit,
        offset=offset
    )


@router.post("", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe_data: RecipeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new recipe (authentication required)
    
    Args:
        recipe_data: Recipe data
        current_user: Authenticated user (from JWT cookie)
        db: Database session
        
    Returns:
        Created recipe
    """
    recipe = RecipeService.create_recipe(db, recipe_data, current_user)
    return RecipeResponse.model_validate(recipe)


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    """
    Get recipe by ID
    
    Args:
        recipe_id: Recipe ID
        db: Database session
        
    Returns:
        Recipe details
        
    Raises:
        HTTPException: If recipe not found
    """
    recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    return RecipeResponse.model_validate(recipe)
