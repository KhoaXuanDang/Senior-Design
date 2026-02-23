from app.db.models import Recipe


def test_save_recipe_to_cookbook(authenticated_client, test_user, db):
    """Test saving a recipe to cookbook"""
    # Create a recipe
    recipe = Recipe(
        title="Test Recipe",
        description="Test",
        ingredients=["ingredient"],
        steps=["step"],
        tags=["test"],
        time_minutes=20,
        difficulty="easy",
        author_id=test_user.id
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    
    # Save to cookbook
    response = authenticated_client.post(f"/cookbook/{recipe.id}")
    assert response.status_code == 201
    assert "message" in response.json()


def test_save_recipe_unauthenticated(client, test_user, db):
    """Test saving recipe without authentication"""
    recipe = Recipe(
        title="Test Recipe",
        description="Test",
        ingredients=["ingredient"],
        steps=["step"],
        tags=["test"],
        time_minutes=20,
        difficulty="easy",
        author_id=test_user.id
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    
    response = client.post(f"/cookbook/{recipe.id}")
    assert response.status_code == 401


def test_save_nonexistent_recipe(authenticated_client):
    """Test saving a recipe that doesn't exist"""
    response = authenticated_client.post("/cookbook/99999")
    assert response.status_code == 404


def test_save_recipe_twice(authenticated_client, test_user, db):
    """Test saving the same recipe twice (should fail)"""
    recipe = Recipe(
        title="Test Recipe",
        description="Test",
        ingredients=["ingredient"],
        steps=["step"],
        tags=["test"],
        time_minutes=20,
        difficulty="easy",
        author_id=test_user.id
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    
    # First save
    response = authenticated_client.post(f"/cookbook/{recipe.id}")
    assert response.status_code == 201
    
    # Second save (should fail)
    response = authenticated_client.post(f"/cookbook/{recipe.id}")
    assert response.status_code == 400
    assert "already saved" in response.json()["detail"].lower()


def test_get_cookbook(authenticated_client, test_user, db):
    """Test getting saved recipes"""
    # Create and save recipes
    recipe1 = Recipe(
        title="Recipe 1",
        description="Test",
        ingredients=["ingredient"],
        steps=["step"],
        tags=["test"],
        time_minutes=20,
        difficulty="easy",
        author_id=test_user.id
    )
    recipe2 = Recipe(
        title="Recipe 2",
        description="Test",
        ingredients=["ingredient"],
        steps=["step"],
        tags=["test"],
        time_minutes=30,
        difficulty="medium",
        author_id=test_user.id
    )
    db.add(recipe1)
    db.add(recipe2)
    db.commit()
    db.refresh(recipe1)
    db.refresh(recipe2)
    
    # Save both recipes
    authenticated_client.post(f"/cookbook/{recipe1.id}")
    authenticated_client.post(f"/cookbook/{recipe2.id}")
    
    # Get cookbook
    response = authenticated_client.get("/cookbook")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    assert all("recipe" in item for item in data)
    assert all("saved_at" in item for item in data)


def test_get_empty_cookbook(authenticated_client):
    """Test getting cookbook when no recipes saved"""
    response = authenticated_client.get("/cookbook")
    assert response.status_code == 200
    assert response.json() == []


def test_get_cookbook_unauthenticated(client):
    """Test getting cookbook without authentication"""
    response = client.get("/cookbook")
    assert response.status_code == 401


def test_remove_recipe_from_cookbook(authenticated_client, test_user, db):
    """Test removing a recipe from cookbook"""
    # Create and save recipe
    recipe = Recipe(
        title="Test Recipe",
        description="Test",
        ingredients=["ingredient"],
        steps=["step"],
        tags=["test"],
        time_minutes=20,
        difficulty="easy",
        author_id=test_user.id
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    
    # Save to cookbook
    authenticated_client.post(f"/cookbook/{recipe.id}")
    
    # Remove from cookbook
    response = authenticated_client.delete(f"/cookbook/{recipe.id}")
    assert response.status_code == 200
    assert "message" in response.json()
    
    # Verify it's removed
    response = authenticated_client.get("/cookbook")
    assert len(response.json()) == 0


def test_remove_unsaved_recipe(authenticated_client, test_user, db):
    """Test removing a recipe that wasn't saved"""
    recipe = Recipe(
        title="Test Recipe",
        description="Test",
        ingredients=["ingredient"],
        steps=["step"],
        tags=["test"],
        time_minutes=20,
        difficulty="easy",
        author_id=test_user.id
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    
    # Try to remove without saving first
    response = authenticated_client.delete(f"/cookbook/{recipe.id}")
    assert response.status_code == 404


def test_remove_recipe_unauthenticated(client, test_user, db):
    """Test removing recipe without authentication"""
    recipe = Recipe(
        title="Test Recipe",
        description="Test",
        ingredients=["ingredient"],
        steps=["step"],
        tags=["test"],
        time_minutes=20,
        difficulty="easy",
        author_id=test_user.id
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    
    response = client.delete(f"/cookbook/{recipe.id}")
    assert response.status_code == 401
