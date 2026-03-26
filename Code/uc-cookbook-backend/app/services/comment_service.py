from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import RecipeComment, Recipe, User
from app.schemas.comment import AddCommentRequest


class CommentService:
    @staticmethod
    def list_comments(db: Session, recipe_id: int) -> List[RecipeComment]:
        return db.query(RecipeComment).filter(
            RecipeComment.recipe_id == recipe_id
        ).order_by(RecipeComment.created_at.asc()).all()

    @staticmethod
    def add_comment(db: Session, recipe: Recipe, user: User, payload: AddCommentRequest) -> RecipeComment:
        comment = RecipeComment(
            recipe_id=recipe.id,
            user_id=user.id,
            content=payload.content,
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def delete_comment(db: Session, recipe: Recipe, comment_id: int, user: User) -> None:
        comment = db.query(RecipeComment).filter(
            RecipeComment.id == comment_id,
            RecipeComment.recipe_id == recipe.id,
        ).first()

        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )

        if comment.user_id != user.id and recipe.author_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this comment"
            )

        db.delete(comment)
        db.commit()
