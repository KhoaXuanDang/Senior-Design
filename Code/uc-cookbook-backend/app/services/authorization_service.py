from typing import Optional
from app.db.models import Recipe, User, Conversation, VisibilityEnum


def can_view_recipe(recipe: Recipe, current_user: Optional[User]) -> bool:
    if current_user and recipe.author_id == current_user.id:
        return True

    return recipe.is_published and recipe.visibility == VisibilityEnum.public


def is_participant(conversation: Conversation, user: User) -> bool:
    return conversation.user_one_id == user.id or conversation.user_two_id == user.id
