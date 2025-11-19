"""User model."""

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, Integer, String, TypeDecorator
from sqlalchemy.engine import Dialect
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import TypeEngine

from my_sqlalchemy.models.base import Base


class UnixTimestampDateTime(TypeDecorator):
    """DateTime type that handles both Unix timestamps (from Prisma) and ISO strings.

    Prisma stores DateTime as Unix timestamp in milliseconds (integer).
    SQLAlchemy by default expects ISO format strings.
    This custom type handles both formats for seamless interoperability.
    """

    impl = DateTime
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine[Any]:
        """Return the native type for this dialect without automatic processing."""
        # Use Integer for SQLite to prevent automatic datetime string processing
        if dialect.name == "sqlite":
            return dialect.type_descriptor(Integer())
        return dialect.type_descriptor(DateTime())

    def process_bind_param(self, value: datetime | None, dialect: Dialect) -> int | None:
        """Convert Python datetime to database value (Unix timestamp for SQLite)."""
        if value is None:
            return None
        # Convert datetime to Unix timestamp in milliseconds for SQLite
        if dialect.name == "sqlite":
            return int(value.timestamp() * 1000)
        return value  # type: ignore[return-value]

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


class User(Base):
    """User model for authentication and user management."""

    __tablename__ = "user"  # Match SQLModel's automatic table name

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        UnixTimestampDateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        UnixTimestampDateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
