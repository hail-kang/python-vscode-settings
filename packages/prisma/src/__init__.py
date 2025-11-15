"""Prisma client package for database access."""

from prisma import Prisma

# Create Prisma client instance
client = Prisma()

__all__ = ["Prisma", "client"]
