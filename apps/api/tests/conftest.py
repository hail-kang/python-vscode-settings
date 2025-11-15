"""Pytest configuration and fixtures."""

from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Import User model to register it with Base
from models import User  # noqa: F401
from models.base import Base

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


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database() -> AsyncGenerator[None, None]:
    """Create tables before each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session for each test."""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
def client(db: AsyncSession) -> Generator[TestClient, None, None]:
    """Create test client with database dependency override."""
    from database import get_db
    from main import app

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
