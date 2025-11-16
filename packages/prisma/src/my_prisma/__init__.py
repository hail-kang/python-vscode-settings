"""Prisma client package for database access."""

from prisma import Prisma

from .manager import PrismaManager

# Create Prisma client instance (deprecated, use PrismaManager instead)
client = Prisma()

__all__ = ["Prisma", "PrismaManager", "client"]
