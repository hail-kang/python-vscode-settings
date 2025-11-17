"""User model using SQLModel."""

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column, Integer, TypeDecorator, func
from sqlalchemy.engine import Dialect
from sqlmodel import Field, SQLModel


class UnixTimestampDateTime(TypeDecorator):
    """DateTime type that handles both Unix timestamps (from Prisma) and ISO strings.

    Prisma stores DateTime as Unix timestamp in milliseconds (integer).
    SQLModel/SQLAlchemy by default expects ISO format strings.
    This custom type handles both formats for seamless interoperability.
    """

    impl = Integer  # SQLite stores as integer
    cache_ok = True

    def process_bind_param(self, value: datetime | None, dialect: Dialect) -> datetime | None:  # noqa: ARG002
        """Convert Python datetime to database value (pass through for SQLite)."""
        return value

    def process_result_value(self, value: Any, dialect: Dialect) -> datetime | None:  # noqa: ARG002, ANN401
        """Convert database value to Python datetime.

        Handles:
        - Unix timestamp in milliseconds (from Prisma): integer -> datetime
        - ISO format string (from SQLAlchemy): string -> datetime
        - Already datetime object: pass through
        """
        if value is None:
            return None

        # If it's already a datetime, return it
        if isinstance(value, datetime):
            return value

        # If it's an integer, treat it as Unix timestamp in milliseconds (Prisma format)
        if isinstance(value, int):
            return datetime.fromtimestamp(value / 1000, tz=timezone.utc)

        # If it's a string, parse it as ISO format
        if isinstance(value, str):
            # Handle SQLite datetime format: "YYYY-MM-DD HH:MM:SS"
            if "T" not in value:
                return datetime.fromisoformat(value.replace(" ", "T"))
            return datetime.fromisoformat(value.replace("Z", "+00:00"))

        return value


class User(SQLModel, table=True):
    """User model with SQLModel (combines SQLAlchemy ORM + Pydantic validation).

    Uses the same database file and table name ('user') as SQLAlchemy,
    but maintains its own metadata registry for independence.
    """

    # SQLModel automatically uses lowercase class name as table name
    # Explicit __tablename__ = "user" causes Pylance type errors
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=100)
    full_name: str | None = Field(default=None, max_length=255)
    hashed_password: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)  # Match SQLAlchemy schema
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            UnixTimestampDateTime,
            server_default=func.current_timestamp(),
            nullable=False,
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            UnixTimestampDateTime,
            server_default=func.current_timestamp(),
            onupdate=func.current_timestamp(),
            nullable=False,
        ),
    )
