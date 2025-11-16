"""FastAPI application entry point."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from database import init_db
from database_sqlmodel import init_db as init_db_sqlmodel
from routers import users_router
from routers.users_prisma import close_prisma, init_prisma
from routers.users_prisma import router as users_prisma_router
from routers.users_sqlmodel import router as users_sqlmodel_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    # Both init_db() calls create the same 'user' table (idempotent)
    await init_db()  # SQLAlchemy tables
    await init_db_sqlmodel()  # SQLModel tables (same schema, same DB file)
    await init_prisma()
    yield
    # Shutdown
    await close_prisma()


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# Include routers
app.include_router(users_router, prefix=settings.api_v1_prefix)
app.include_router(users_prisma_router, prefix=settings.api_v1_prefix)
app.include_router(users_sqlmodel_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Python VSCode Settings API", "version": settings.app_version}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
