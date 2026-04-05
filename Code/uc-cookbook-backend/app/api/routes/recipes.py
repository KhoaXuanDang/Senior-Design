from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.api.deps import get_current_user, get_current_user_optional
from app.schemas.recipe import CreateRecipeRequest, UpdateRecipeRequest, RecipeResponse, RecipesResponse
from app.services.recipe_service import RecipeService
from app.services.authorization_service import can_view_recipe

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
    
    # Build responses and include fork_count for each recipe
    recipe_responses = []
    from app.db.models import Recipe as RecipeModel
    for r in recipes:
        res = RecipeResponse.model_validate(r)
        # compute fork count (number of recipes that reference this as origin)
        fork_count = db.query(RecipeModel).filter(RecipeModel.origin_recipe_id == r.id).count()
        res.fork_count = fork_count
        recipe_responses.append(res)

    return RecipesResponse(
        recipes=recipe_responses,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe_data: CreateRecipeRequest,
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
    resp = RecipeResponse.model_validate(recipe)
    from app.db.models import Recipe as RecipeModel
    resp.fork_count = db.query(RecipeModel).filter(RecipeModel.origin_recipe_id == recipe.id).count()
    return resp


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(
    recipe_id: int,
    current_user: Optional[User] = Depends(get_current_user_optional),
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

    if not can_view_recipe(recipe, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this recipe"
        )
    
    resp = RecipeResponse.model_validate(recipe)
    from app.db.models import Recipe as RecipeModel
    resp.fork_count = db.query(RecipeModel).filter(RecipeModel.origin_recipe_id == recipe.id).count()
    return resp


@router.put("/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(
    recipe_id: int,
    recipe_data: UpdateRecipeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recipe = RecipeService.get_recipe_by_id(db, recipe_id)

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )

    recipe = RecipeService.update_recipe(db, recipe, recipe_data, current_user)
    return RecipeResponse.model_validate(recipe)


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    recipe_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )
    RecipeService.delete_recipe(db, recipe, current_user)
