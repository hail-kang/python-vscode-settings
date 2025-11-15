"""Database connection and session management."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings

# Convert database URL to async version
database_url = settings.database_url
if database_url.startswith("sqlite"):
    database_url = database_url.replace("sqlite://", "sqlite+aiosqlite://")
elif database_url.startswith("postgresql"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")

# Create async database engine
engine = create_async_engine(
    database_url,
    echo=settings.debug,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session dependency."""
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    """Initialize database tables."""
    from my_sqlalchemy.models.base import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
