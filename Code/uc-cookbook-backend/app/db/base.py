# Import all models here for Alembic auto-detection
from app.db.session import Base
from app.db.models import User, Recipe, CookbookSave

__all__ = ["Base", "User", "Recipe", "CookbookSave"]
