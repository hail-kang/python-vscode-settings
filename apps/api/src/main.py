"""FastAPI application entry point."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from database import init_db
from routers import users_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    await init_db()
    yield
    # Shutdown (cleanup if needed)


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# Include routers
app.include_router(users_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Python VSCode Settings API", "version": settings.app_version}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
