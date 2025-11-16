"""Pytest configuration and fixtures."""

from collections.abc import AsyncGenerator, Generator

from fastapi.testclient import TestClient
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

# Import User model to register it with Base
from my_sqlalchemy.models import User  # noqa: F401  # type: ignore[reportUnusedImport]
from my_sqlalchemy.models.base import Base

# Import SQLModel User to register it
from my_sqlmodel.models import (
    User as SQLModelUser,  # noqa: F401  # type: ignore[reportUnusedImport]
)

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
)
TestingSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# SQLModel engine for testing
sqlmodel_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
)
SQLModelTestingSessionLocal = async_sessionmaker(
    sqlmodel_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database() -> AsyncGenerator[None, None]:
    """Create tables before each test."""
    # Create SQLAlchemy tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create SQLModel tables
    async with sqlmodel_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    # Drop SQLAlchemy tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Drop SQLModel tables
    async with sqlmodel_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session for each test."""
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def sqlmodel_db() -> AsyncGenerator[AsyncSession, None]:
    """Create test SQLModel database session for each test."""
    async with SQLModelTestingSessionLocal() as session:
        yield session


@pytest.fixture
def client(db: AsyncSession, sqlmodel_db: AsyncSession) -> Generator[TestClient, None, None]:
    """Create test client with database dependency override."""
    from database import get_db
    from database_sqlmodel import get_db as get_sqlmodel_db
    from main import app

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db

    async def override_get_sqlmodel_db() -> AsyncGenerator[AsyncSession, None]:
        yield sqlmodel_db

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_sqlmodel_db] = override_get_sqlmodel_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
