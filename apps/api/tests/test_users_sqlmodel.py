"""Tests for SQLModel user endpoints."""

from fastapi import status
from fastapi.testclient import TestClient


def test_create_user(client: TestClient) -> None:
    """Test creating a new user."""
    response = client.post(
        "/api/v1/sqlmodel/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "hashed_password": "hashedpassword123",
            "is_active": True,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "created_at" in data


def test_create_user_duplicate_email(client: TestClient) -> None:
    """Test creating a user with duplicate email."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "hashed_password": "hashedpassword123",
    }
    # Create first user
    client.post("/api/v1/sqlmodel/users/", json=user_data)

    # Try to create second user with same email
    user_data["username"] = "different_username"
    response = client.post("/api/v1/sqlmodel/users/", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email already registered"


def test_create_user_duplicate_username(client: TestClient) -> None:
    """Test creating a user with duplicate username."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "hashed_password": "hashedpassword123",
    }
    # Create first user
    client.post("/api/v1/sqlmodel/users/", json=user_data)

    # Try to create second user with same username
    user_data["email"] = "different@example.com"
    response = client.post("/api/v1/sqlmodel/users/", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Username already taken"


def test_get_user(client: TestClient) -> None:
    """Test getting a user by ID."""
    # Create a user
    create_response = client.post(
        "/api/v1/sqlmodel/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "hashed_password": "hashedpassword123",
        },
    )
    user_id = create_response.json()["id"]

    # Get the user
    response = client.get(f"/api/v1/sqlmodel/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "test@example.com"


def test_get_user_not_found(client: TestClient) -> None:
    """Test getting a non-existent user."""
    response = client.get("/api/v1/sqlmodel/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_list_users(client: TestClient) -> None:
    """Test listing all users."""
    # Create multiple users
    for i in range(3):
        client.post(
            "/api/v1/sqlmodel/users/",
            json={
                "email": f"test{i}@example.com",
                "username": f"testuser{i}",
                "hashed_password": "hashedpassword123",
            },
        )

    # List users
    response = client.get("/api/v1/sqlmodel/users/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3
    # List response only returns id, username, created_at
    assert "id" in data[0]
    assert "username" in data[0]
    assert "created_at" in data[0]
    assert "email" not in data[0]  # email should not be in list response


def test_list_users_pagination(client: TestClient) -> None:
    """Test listing users with pagination."""
    # Create multiple users
    for i in range(5):
        client.post(
            "/api/v1/sqlmodel/users/",
            json={
                "email": f"test{i}@example.com",
                "username": f"testuser{i}",
                "hashed_password": "hashedpassword123",
            },
        )

    # List with pagination
    response = client.get("/api/v1/sqlmodel/users/?skip=2&limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    # List response only returns minimal fields
    assert "id" in data[0]
    assert "username" in data[0]
    assert "created_at" in data[0]


def test_update_user(client: TestClient) -> None:
    """Test updating a user."""
    # Create a user
    create_response = client.post(
        "/api/v1/sqlmodel/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "hashed_password": "hashedpassword123",
        },
    )
    user_id = create_response.json()["id"]

    # Update the user
    response = client.patch(
        f"/api/v1/sqlmodel/users/{user_id}",
        json={"full_name": "Updated Name", "is_active": False},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["is_active"] is False
    assert data["email"] == "test@example.com"  # Unchanged


def test_update_user_not_found(client: TestClient) -> None:
    """Test updating a non-existent user."""
    response = client.patch("/api/v1/sqlmodel/users/999", json={"full_name": "New Name"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user(client: TestClient) -> None:
    """Test deleting a user."""
    # Create a user
    create_response = client.post(
        "/api/v1/sqlmodel/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "hashed_password": "hashedpassword123",
        },
    )
    user_id = create_response.json()["id"]

    # Delete the user
    response = client.delete(f"/api/v1/sqlmodel/users/{user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify deletion
    get_response = client.get(f"/api/v1/sqlmodel/users/{user_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user_not_found(client: TestClient) -> None:
    """Test deleting a non-existent user."""
    response = client.delete("/api/v1/sqlmodel/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
