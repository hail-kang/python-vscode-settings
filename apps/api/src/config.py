"""Application configuration."""

import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the project root directory (apps/api/)
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "app.db"


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

    # Database - use absolute paths to ensure both ORMs use the same file
    database_url: str = f"sqlite:///{DB_PATH}"
    # Prisma uses the same database file
    prisma_database_url: str = f"file:{DB_PATH}"

    # API
    api_v1_prefix: str = "/api/v1"


settings = Settings()

# Set DATABASE_URL environment variable for Prisma
os.environ.setdefault("DATABASE_URL", settings.prisma_database_url)
