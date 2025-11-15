"""Shared SQLAlchemy models package."""

__version__ = "0.1.0"

from my_sqlalchemy.models.base import Base
from my_sqlalchemy.models.user import User

__all__ = ["Base", "User"]
