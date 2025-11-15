"""Application configuration."""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Python VSCode Settings API"
    app_version: str = "0.1.0"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./app.db"
    prisma_database_url: str = "file:../../packages/prisma/dev.db"

    # API
    api_v1_prefix: str = "/api/v1"


settings = Settings()

# Set DATABASE_URL environment variable for Prisma
os.environ.setdefault("DATABASE_URL", settings.prisma_database_url)
