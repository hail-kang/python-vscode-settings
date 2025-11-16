"""User API endpoints using Prisma ORM."""

from fastapi import APIRouter, Depends, HTTPException, status
from prisma import Prisma
from prisma.errors import UniqueViolationError

from my_prisma import PrismaManager
from schemas import UserCreate, UserListItem, UserResponse, UserUpdate

router = APIRouter(prefix="/prisma/users", tags=["users-prisma"])


async def get_prisma_client() -> Prisma:
    """Get Prisma client instance as a dependency."""
    return PrismaManager.get()


async def init_prisma() -> None:
    """Initialize Prisma client (called from lifespan)."""
    await PrismaManager.init()


async def close_prisma() -> None:
    """Close Prisma client (called from lifespan)."""
    await PrismaManager.close()


def prisma_to_response(prisma_user: dict) -> dict:
    """Convert Prisma camelCase to snake_case for response schema."""
    return {
        "id": prisma_user["id"],
        "email": prisma_user["email"],
        "username": prisma_user["username"],
        "full_name": prisma_user.get("fullName"),
        "is_active": prisma_user["isActive"],
        "created_at": prisma_user["createdAt"],
        "updated_at": prisma_user["updatedAt"],
    }


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, prisma: Prisma = Depends(get_prisma_client)) -> dict:
    """Create a new user using Prisma."""

    try:
        new_user = await prisma.user.create(
            data={
                "email": user.email,
                "username": user.username,
                "fullName": user.full_name,
                "hashedPassword": user.hashed_password,  # In production, hash the password!
                "isActive": user.is_active,
            }
        )
        return prisma_to_response(new_user.model_dump())
    except UniqueViolationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered",
        ) from e


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, prisma: Prisma = Depends(get_prisma_client)) -> dict:
    """Get a user by ID using Prisma."""

    db_user = await prisma.user.find_unique(where={"id": user_id})
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return prisma_to_response(db_user.model_dump())


@router.get("/", response_model=list[UserListItem])
async def list_users(
    skip: int = 0, limit: int = 100, prisma: Prisma = Depends(get_prisma_client)
) -> list[UserListItem]:
    """List all users with pagination using Prisma (returns minimal fields)."""

    users = await prisma.user.find_many(
        skip=skip,
        take=limit,
    )
    # Return only minimal fields for list response
    return [
        UserListItem(id=user.id, username=user.username, created_at=user.createdAt)
        for user in users
    ]


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, user_update: UserUpdate, prisma: Prisma = Depends(get_prisma_client)
) -> dict:
    """Update a user using Prisma."""

    # Check if user exists
    db_user = await prisma.user.find_unique(where={"id": user_id})
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Convert snake_case to camelCase for Prisma
    update_data: dict = {}
    field_mapping = {
        "email": "email",
        "username": "username",
        "full_name": "fullName",
        "hashed_password": "hashedPassword",
        "is_active": "isActive",
        "is_superuser": "isSuperuser",
    }

    for field, value in user_update.model_dump(exclude_unset=True).items():
        if field in field_mapping:
            update_data[field_mapping[field]] = value

    try:
        updated_user = await prisma.user.update(
            where={"id": user_id},
            data=update_data,  # type: ignore[arg-type]
        )
        if updated_user:
            return prisma_to_response(updated_user.model_dump())
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    except UniqueViolationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already taken",
        ) from e


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, prisma: Prisma = Depends(get_prisma_client)) -> None:
    """Delete a user using Prisma."""

    # Check if user exists
    db_user = await prisma.user.find_unique(where={"id": user_id})
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await prisma.user.delete(where={"id": user_id})
