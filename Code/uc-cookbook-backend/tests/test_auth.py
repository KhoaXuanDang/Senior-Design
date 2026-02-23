def test_register_user(client):
    """Test user registration"""
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@mail.uc.edu",
            "username": "new_user",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "user" in data
    assert data["user"]["email"] == "newuser@mail.uc.edu"
    assert data["user"]["username"] == "new_user"
    assert "id" in data["user"]
    assert "password" not in data["user"]
    
    # Check that cookie was set
    assert "access_token" in response.cookies


def test_register_duplicate_email(client, test_user):
    """Test registration with existing email"""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@mail.uc.edu",  # Already exists
            "username": "another_user",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post(
        "/auth/login",
        json={
            "email": "test@mail.uc.edu",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert data["user"]["email"] == "test@mail.uc.edu"
    
    # Check that cookie was set
    assert "access_token" in response.cookies


def test_login_wrong_password(client, test_user):
    """Test login with wrong password"""
    response = client.post(
        "/auth/login",
        json={
            "email": "test@mail.uc.edu",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


def test_login_nonexistent_user(client):
    """Test login with nonexistent email"""
    response = client.post(
        "/auth/login",
        json={
            "email": "nonexistent@mail.uc.edu",
            "password": "password123"
        }
    )
    assert response.status_code == 401


def test_logout(authenticated_client):
    """Test logout"""
    response = authenticated_client.post("/auth/logout")
    assert response.status_code == 200
    assert "message" in response.json()
