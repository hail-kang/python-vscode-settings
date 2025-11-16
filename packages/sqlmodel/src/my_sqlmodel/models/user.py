"""User model using SQLModel."""

from datetime import datetime

from sqlmodel import Field, SQLModel


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
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
