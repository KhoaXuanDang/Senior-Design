from collections import defaultdict
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload, selectinload
from app.db.models import CommentReaction, RecipeComment, Recipe, User
from app.schemas.auth import AuthorResponse
from app.schemas.comment import (
    AddCommentRequest,
    ALLOWED_COMMENT_EMOJIS,
    ReactionSummary,
    RecipeCommentResponse,
)


def _reaction_summaries(
    rows: List[CommentReaction],
    current_user_id: Optional[int],
) -> List[ReactionSummary]:
    by_emoji: dict[str, list[int]] = defaultdict(list)
    for r in rows:
        by_emoji[r.emoji].append(r.user_id)
    out: List[ReactionSummary] = []
    for emoji in sorted(by_emoji.keys()):
        user_ids = by_emoji[emoji]
        out.append(
            ReactionSummary(
                emoji=emoji,
                count=len(user_ids),
                reacted_by_me=current_user_id is not None and current_user_id in user_ids,
            )
        )
    return out


def _to_response(
    comment: RecipeComment,
    current_user_id: Optional[int],
) -> RecipeCommentResponse:
    rows = list(comment.comment_reactions) if comment.comment_reactions else []
    return RecipeCommentResponse(
        id=comment.id,
        recipe_id=comment.recipe_id,
        user_id=comment.user_id,
        parent_id=comment.parent_id,
        content=comment.content,
        created_at=comment.created_at,
        user=AuthorResponse.model_validate(comment.user) if comment.user else None,
        reactions=_reaction_summaries(rows, current_user_id),
    )


class CommentService:
    @staticmethod
    def list_comments(
        db: Session,
        recipe_id: int,
        current_user_id: Optional[int],
    ) -> List[RecipeCommentResponse]:
        comments = (
            db.query(RecipeComment)
            .options(
                joinedload(RecipeComment.user),
                selectinload(RecipeComment.comment_reactions),
            )
            .filter(RecipeComment.recipe_id == recipe_id)
            .order_by(RecipeComment.created_at.asc())
            .all()
        )
        return [_to_response(c, current_user_id) for c in comments]

    @staticmethod
    def add_comment(
        db: Session,
        recipe: Recipe,
        user: User,
        payload: AddCommentRequest,
    ) -> RecipeCommentResponse:
        parent_id = payload.parent_id
        if parent_id is not None:
            parent = (
                db.query(RecipeComment)
                .filter(
                    RecipeComment.id == parent_id,
                    RecipeComment.recipe_id == recipe.id,
                )
                .first()
            )
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent comment not found",
                )

        comment = RecipeComment(
            recipe_id=recipe.id,
            user_id=user.id,
            parent_id=parent_id,
            content=payload.content,
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        comment = (
            db.query(RecipeComment)
            .options(
                joinedload(RecipeComment.user),
                selectinload(RecipeComment.comment_reactions),
            )
            .filter(RecipeComment.id == comment.id)
            .first()
        )
        return _to_response(comment, user.id)

    @staticmethod
    def set_reaction(
        db: Session,
        recipe: Recipe,
        comment_id: int,
        user: User,
        emoji: str,
    ) -> RecipeCommentResponse:
        if emoji not in ALLOWED_COMMENT_EMOJIS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Emoji must be one of: {', '.join(sorted(ALLOWED_COMMENT_EMOJIS))}",
            )

        comment = (
            db.query(RecipeComment)
            .filter(
                RecipeComment.id == comment_id,
                RecipeComment.recipe_id == recipe.id,
            )
            .first()
        )
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )

        existing = (
            db.query(CommentReaction)
            .filter(
                CommentReaction.comment_id == comment.id,
                CommentReaction.user_id == user.id,
            )
            .first()
        )
        if existing:
            if existing.emoji == emoji:
                db.delete(existing)
            else:
                existing.emoji = emoji
        else:
            db.add(
                CommentReaction(
                    comment_id=comment.id,
                    user_id=user.id,
                    emoji=emoji,
                )
            )
        db.commit()

        comment = (
            db.query(RecipeComment)
            .options(
                joinedload(RecipeComment.user),
                selectinload(RecipeComment.comment_reactions),
            )
            .filter(RecipeComment.id == comment_id)
            .first()
        )
        return _to_response(comment, user.id)

    @staticmethod
    def delete_comment(db: Session, recipe: Recipe, comment_id: int, user: User) -> None:
        comment = db.query(RecipeComment).filter(
            RecipeComment.id == comment_id,
            RecipeComment.recipe_id == recipe.id,
        ).first()

        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )

        if comment.user_id != user.id and recipe.author_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this comment",
            )

        db.delete(comment)
        db.commit()
