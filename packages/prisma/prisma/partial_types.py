"""Partial type definitions for Prisma models.

According to Prisma Python docs, partials should be created using:
Model.create_partial(name, include/exclude, ...)

This module exports pre-defined partial types for convenience.
"""

from prisma.models import User

# Create a partial type for list endpoints - only id, username, created_at
UserMinimal = User.create_partial(
    "UserMinimal",
    include={"id", "username", "created_at"},
)

__all__ = ["UserMinimal"]
