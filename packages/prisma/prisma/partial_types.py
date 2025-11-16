"""Partial type definitions for Prisma models.

This file is executed during `prisma generate` to create partial types.
"""

from prisma.models import User

# Create a partial type for list endpoints - only id, username, created_at
UserMinimal = User.create_partial(
    "UserMinimal",
    include={"id", "username", "created_at"},
)
