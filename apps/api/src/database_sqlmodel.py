"""SQLModel async database setup.

SQLModel shares the same database file and table name ('user') as SQLAlchemy,
but uses its own metadata registry. Both ORMs can read/write to the same tables.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from config import settings

# Create async engine using the same database URL as SQLAlchemy
# Convert sqlite:/// to sqlite+aiosqlite:///
database_url = settings.database_url.replace("sqlite:///", "sqlite+aiosqlite:///")

engine = create_async_engine(
    database_url,
    echo=False,
    connect_args={"check_same_thread": False},  # Only for SQLite
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    """Initialize database tables for SQLModel.

    Creates the 'user' table if it doesn't exist. Since SQLAlchemy also creates
    a 'user' table with the same schema, this is idempotent.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database sessions."""
    async with AsyncSessionLocal() as session:
        yield session
