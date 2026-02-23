from app.db.models import Recipe


def test_create_recipe_authenticated(authenticated_client):
    """Test creating a recipe when authenticated"""
    recipe_data = {
        "title": "Test Recipe",
        "description": "A test recipe description",
        "ingredients": ["ingredient 1", "ingredient 2", "ingredient 3"],
        "steps": ["step 1", "step 2", "step 3"],
        "tags": ["test", "quick"],
        "time_minutes": 30,
        "difficulty": "easy",
        "image_url": "https://example.com/image.jpg"
    }
    
    response = authenticated_client.post("/recipes", json=recipe_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == recipe_data["title"]
    assert data["description"] == recipe_data["description"]
    assert data["ingredients"] == recipe_data["ingredients"]
    assert data["steps"] == recipe_data["steps"]
    assert data["tags"] == recipe_data["tags"]
    assert data["time_minutes"] == recipe_data["time_minutes"]
    assert data["difficulty"] == recipe_data["difficulty"]
    assert "id" in data
    assert "author_id" in data
    assert "created_at" in data


def test_create_recipe_unauthenticated(client):
    """Test creating a recipe without authentication"""
    recipe_data = {
        "title": "Test Recipe",
        "description": "A test recipe",
        "ingredients": ["ingredient 1"],
        "steps": ["step 1"],
        "tags": [],
        "time_minutes": 30,
        "difficulty": "easy"
    }
    
    response = client.post("/recipes", json=recipe_data)
    assert response.status_code == 401


def test_get_recipes_list(client, authenticated_client, test_user, db):
    """Test getting list of recipes"""
    # Create some test recipes
    recipe1 = Recipe(
        title="Easy Pasta",
        description="Quick pasta recipe",
        ingredients=["pasta", "sauce"],
        steps=["cook pasta", "add sauce"],
        tags=["pasta", "easy"],
        time_minutes=20,
        difficulty="easy",
        author_id=test_user.id
    )
    recipe2 = Recipe(
        title="Medium Stir Fry",
        description="Asian stir fry",
        ingredients=["vegetables", "soy sauce"],
        steps=["chop vegetables", "stir fry"],
        tags=["asian", "healthy"],
        time_minutes=30,
        difficulty="medium",
        author_id=test_user.id
    )
    db.add(recipe1)
    db.add(recipe2)
    db.commit()
    
    response = client.get("/recipes")
    assert response.status_code == 200
    
    data = response.json()
    assert "recipes" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert data["total"] == 2
    assert len(data["recipes"]) == 2


def test_get_recipes_with_search(client, authenticated_client, test_user, db):
    """Test searching recipes"""
    recipe = Recipe(
        title="Special Pasta Dish",
        description="A unique pasta recipe",
        ingredients=["pasta"],
        steps=["cook"],
        tags=["pasta"],
        time_minutes=20,
        difficulty="easy",
        author_id=test_user.id
    )
    db.add(recipe)
    db.commit()
    
    response = client.get("/recipes?search=pasta")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] >= 1
    assert any("pasta" in r["title"].lower() for r in data["recipes"])


def test_get_recipes_with_difficulty_filter(client, authenticated_client, test_user, db):
    """Test filtering recipes by difficulty"""
    recipe = Recipe(
        title="Hard Recipe",
        description="Complex recipe",
        ingredients=["many", "ingredients"],
        steps=["many", "steps"],
        tags=["advanced"],
        time_minutes=120,
        difficulty="hard",
        author_id=test_user.id
    )
    db.add(recipe)
    db.commit()
    
    response = client.get("/recipes?difficulty=hard")
    assert response.status_code == 200
    
    data = response.json()
    assert all(r["difficulty"] == "hard" for r in data["recipes"])


def test_get_recipe_by_id(client, authenticated_client, test_user, db):
    """Test getting a specific recipe"""
    recipe = Recipe(
        title="Test Recipe",
        description="Test description",
        ingredients=["ingredient 1"],
        steps=["step 1"],
        tags=["test"],
        time_minutes=20,
        difficulty="easy",
        author_id=test_user.id
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    
    response = client.get(f"/recipes/{recipe.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == recipe.id
    assert data["title"] == recipe.title


def test_get_nonexistent_recipe(client):
    """Test getting a recipe that doesn't exist"""
    response = client.get("/recipes/99999")
    assert response.status_code == 404


def test_pagination(client, authenticated_client, test_user, db):
    """Test recipe pagination"""
    # Create 25 recipes
    for i in range(25):
        recipe = Recipe(
            title=f"Recipe {i}",
            description=f"Description {i}",
            ingredients=["ingredient"],
            steps=["step"],
            tags=["test"],
            time_minutes=20,
            difficulty="easy",
            author_id=test_user.id
        )
        db.add(recipe)
    db.commit()
    
    # Test first page
    response = client.get("/recipes?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["recipes"]) == 10
    assert data["total"] == 25
    assert data["limit"] == 10
    assert data["offset"] == 0
    
    # Test second page
    response = client.get("/recipes?limit=10&offset=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["recipes"]) == 10
    assert data["offset"] == 10
