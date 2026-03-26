from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_current_user_optional
from app.db.models import User
from app.db.session import get_db
from app.schemas.comment import AddCommentRequest, RecipeCommentResponse
from app.schemas.common import SuccessResponse
from app.services.authorization_service import can_view_recipe
from app.services.comment_service import CommentService
from app.services.recipe_service import RecipeService


router = APIRouter(prefix="/recipes", tags=["Comments"])


@router.get("/{recipe_id}/comments", response_model=List[RecipeCommentResponse])
async def list_comments(
    recipe_id: int,
    current_user: User | None = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    if not can_view_recipe(recipe, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this recipe")

    comments = CommentService.list_comments(db, recipe_id)
    return [RecipeCommentResponse.model_validate(comment) for comment in comments]


@router.post("/{recipe_id}/comments", response_model=RecipeCommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    recipe_id: int,
    payload: AddCommentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    if not can_view_recipe(recipe, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this recipe")

    comment = CommentService.add_comment(db, recipe, current_user, payload)
    return RecipeCommentResponse.model_validate(comment)


@router.delete("/{recipe_id}/comments/{comment_id}", response_model=SuccessResponse)
async def delete_comment(
    recipe_id: int,
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    if not can_view_recipe(recipe, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this recipe")

    CommentService.delete_comment(db, recipe, comment_id, current_user)
    return SuccessResponse(message="Comment deleted")
