"""User API endpoints using Prisma ORM."""

from fastapi import APIRouter, Depends, HTTPException, status
from prisma import Prisma
from prisma.errors import UniqueViolationError
from prisma.partials import UserMinimal

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
    """Convert Prisma model to response schema (now using snake_case)."""
    return {
        "id": prisma_user["id"],
        "email": prisma_user["email"],
        "username": prisma_user["username"],
        "full_name": prisma_user.get("full_name"),
        "is_active": prisma_user["is_active"],
        "created_at": prisma_user["created_at"],
        "updated_at": prisma_user["updated_at"],
    }


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, prisma: Prisma = Depends(get_prisma_client)) -> dict:
    """Create a new user using Prisma."""

    try:
        new_user = await prisma.user.create(
            data={
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "hashed_password": user.hashed_password,  # In production, hash the password!
                "is_active": user.is_active,
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
    """List all users with pagination using Prisma with field-level SELECT."""
    # Use partial type to select only needed fields at DB level
    users = await UserMinimal.prisma(prisma).find_many(
        skip=skip,
        take=limit,
    )
    # Return only minimal fields for list response
    return [
        UserListItem(id=user.id, username=user.username, created_at=user.created_at)
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

    # Build update data (now using snake_case, no conversion needed)
    update_data = user_update.model_dump(exclude_unset=True)

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
