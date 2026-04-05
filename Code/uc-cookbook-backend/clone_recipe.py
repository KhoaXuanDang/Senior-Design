"""Simple dev script: clone an existing recipe by copying fields and
setting structured attribution fields (`origin_recipe_id`, `origin_author_id`).

Usage: run with the backend venv python from the project root:
  .\env\Scripts\python.exe clone_recipe.py <source_recipe_id> <new_author_id>

This script is for local dev smoke-tests only.
"""
import sys
from app.db.session import SessionLocal
from app.db.models import Recipe

def clone_recipe(source_id: int, new_author_id: int):
    db = SessionLocal()
    try:
        src = db.query(Recipe).filter(Recipe.id == source_id).first()
        if not src:
            print('Source recipe not found:', source_id)
            return None

        new = Recipe(
            title=f"Fork of {src.title}",
            description=src.description,
            ingredients=list(src.ingredients) if src.ingredients is not None else [],
            steps=list(src.steps) if src.steps is not None else [],
            tags=list(src.tags) if src.tags is not None else [],
            time_minutes=src.time_minutes,
            difficulty=src.difficulty,
            image_url=src.image_url,
            is_published=src.is_published,
            visibility=src.visibility,
            author_id=new_author_id,
            origin_recipe_id=src.id,
            origin_author_id=src.author_id,
        )

        db.add(new)
        db.commit()
        db.refresh(new)

        # compute fork_count for source
        fc = db.query(Recipe).filter(Recipe.origin_recipe_id == src.id).count()
        print(f'Cloned recipe id={new.id} from source={src.id}; fork_count={fc}')
        return new
    finally:
        db.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: clone_recipe.py <source_recipe_id> <new_author_id>')
        sys.exit(1)
    src_id = int(sys.argv[1])
    new_author = int(sys.argv[2])
    clone_recipe(src_id, new_author)
