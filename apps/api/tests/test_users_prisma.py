"""Tests for Prisma-based user endpoints."""

from collections.abc import AsyncGenerator

import httpx
import pytest
import pytest_asyncio
from prisma import Prisma

from main import app


@pytest_asyncio.fixture
async def prisma_client() -> AsyncGenerator[Prisma, None]:
    """Create Prisma client for testing."""
    import os

    # Use the dev.db that was created by prisma migrate
    test_db = "file:../../packages/prisma/dev.db"
    original_url = os.environ.get("DATABASE_URL")
    os.environ["DATABASE_URL"] = test_db

    client = Prisma()
    await client.connect()

    # Clean up database before test
    await client.user.delete_many()

    yield client

    # Clean up database after test
    await client.user.delete_many()
    await client.disconnect()

    # Restore original DATABASE_URL
    if original_url:
        os.environ["DATABASE_URL"] = original_url
    else:
        os.environ.pop("DATABASE_URL", None)


@pytest.mark.asyncio
async def test_create_user_prisma(prisma_client: Prisma) -> None:  # noqa: ARG001
    """Test creating a user with Prisma."""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/api/v1/prisma/users/",
            json={
                "email": "prisma@example.com",
                "username": "prismauser",
                "full_name": "Prisma User",
                "hashed_password": "hashedpass123",
                "is_active": True,
            },
        )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "prisma@example.com"
    assert data["username"] == "prismauser"
    assert data["full_name"] == "Prisma User"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_user_prisma(prisma_client: Prisma) -> None:
    """Test getting a user by ID with Prisma."""
    # Create a user first
    user = await prisma_client.user.create(
        data={
            "email": "get@example.com",
            "username": "getuser",
            "fullName": "Get User",
            "hashedPassword": "hashedpass123",
            "isActive": True,
        }
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get(f"/api/v1/prisma/users/{user.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "get@example.com"
    assert data["username"] == "getuser"


@pytest.mark.asyncio
async def test_get_user_not_found_prisma(prisma_client: Prisma) -> None:
    """Test getting a non-existent user with Prisma."""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/api/v1/prisma/users/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_list_users_prisma(prisma_client: Prisma) -> None:
    """Test listing users with Prisma."""
    # Create multiple users
    await prisma_client.user.create(
        data={
            "email": "user1@example.com",
            "username": "user1",
            "fullName": "User One",
            "hashedPassword": "hashedpass123",
            "isActive": True,
        }
    )
    await prisma_client.user.create(
        data={
            "email": "user2@example.com",
            "username": "user2",
            "fullName": "User Two",
            "hashedPassword": "hashedpass123",
            "isActive": True,
        }
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/api/v1/prisma/users/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["email"] == "user1@example.com"
    assert data[1]["email"] == "user2@example.com"


@pytest.mark.asyncio
async def test_update_user_prisma(prisma_client: Prisma) -> None:
    """Test updating a user with Prisma."""
    # Create a user first
    user = await prisma_client.user.create(
        data={
            "email": "update@example.com",
            "username": "updateuser",
            "fullName": "Update User",
            "hashedPassword": "hashedpass123",
            "isActive": True,
        }
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.patch(
            f"/api/v1/prisma/users/{user.id}",
            json={"full_name": "Updated Name", "is_active": False},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["is_active"] is False
    assert data["email"] == "update@example.com"  # Unchanged


@pytest.mark.asyncio
async def test_delete_user_prisma(prisma_client: Prisma) -> None:
    """Test deleting a user with Prisma."""
    # Create a user first
    user = await prisma_client.user.create(
        data={
            "email": "delete@example.com",
            "username": "deleteuser",
            "fullName": "Delete User",
            "hashedPassword": "hashedpass123",
            "isActive": True,
        }
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.delete(f"/api/v1/prisma/users/{user.id}")

    assert response.status_code == 204

    # Verify user is deleted
    deleted_user = await prisma_client.user.find_unique(where={"id": user.id})
    assert deleted_user is None


@pytest.mark.asyncio
async def test_create_user_duplicate_email_prisma(prisma_client: Prisma) -> None:
    """Test creating a user with duplicate email using Prisma."""
    # Create first user
    await prisma_client.user.create(
        data={
            "email": "duplicate@example.com",
            "username": "user1",
            "fullName": "User One",
            "hashedPassword": "hashedpass123",
            "isActive": True,
        }
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/api/v1/prisma/users/",
            json={
                "email": "duplicate@example.com",
                "username": "user2",
                "full_name": "User Two",
                "hashed_password": "hashedpass123",
                "is_active": True,
            },
        )

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]
