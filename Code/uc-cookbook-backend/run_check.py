"""run_check.py — consolidated developer checks for the backend

This script performs quick, readable smoke checks useful during local
development. It runs two checks:

1. DB check: queries published public recipes via the service layer and
   prints each recipe id, origin id and computed fork_count.
2. API check: uses FastAPI TestClient to request the `/recipes` route and
   pretty-prints the JSON response (status and top-level summary).

Usage (from project root, inside the backend venv):
  .\env\Scripts\python.exe run_check.py

The script is intentionally safe for dev use only.
"""

import json
import traceback
import sys
from typing import Any

from app.db.session import SessionLocal
from app.services.recipe_service import RecipeService
from app.db.models import Recipe as RecipeModel


def db_check():
    db = SessionLocal()
    try:
        print('=== DB CHECK: recipes via service layer ===')
        recipes, total = RecipeService.get_recipes(db)
        print(f'Total (service query): {total}\n')
        for r in recipes:
            rid = getattr(r, 'id', None)
            origin = getattr(r, 'origin_recipe_id', None)
            try:
                fc = db.query(RecipeModel).filter(RecipeModel.origin_recipe_id == rid).count()
            except Exception:
                fc = '<error>'
            print(f'- id={rid} origin={origin} fork_count={fc}')
    except Exception:
        print('DB check failed:')
        traceback.print_exc()
    finally:
        db.close()


def api_check():
    print('\n=== API CHECK: GET /recipes via TestClient ===')
    try:
        # Import here so running this script doesn't require TestClient unless used
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)
        resp = client.get('/recipes')
        print(f'Status: {resp.status_code}')
        try:
            body = resp.json()
            # Print a short summary and the first recipe (if any)
            summary = {
                'total': body.get('total'),
                'limit': body.get('limit'),
                'offset': body.get('offset'),
                'count_returned': len(body.get('recipes', [])),
            }
            print('Summary:', json.dumps(summary, indent=2))
            if body.get('recipes'):
                print('\nFirst recipe (pretty):')
                print(json.dumps(body['recipes'][0], indent=2))
        except Exception:
            print('Failed to parse JSON response')
            print(resp.text[:1000])
    except Exception:
        print('API check failed:')
        traceback.print_exc()


def main():
    db_check()
    api_check()


if __name__ == '__main__':
    main()
