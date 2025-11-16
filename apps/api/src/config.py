"""Application configuration."""

import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the apps/api directory (parent of src/)
API_DIR = Path(__file__).parent.parent
ENV_FILE = API_DIR / ".env"


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Python VSCode Settings API"
    app_version: str = "0.1.0"
    debug: bool = False

    # Database - DB_PATH should be set via environment variable
    db_path: str = ""

    # API
    api_v1_prefix: str = "/api/v1"

    @property
    def database_url(self) -> str:
        """SQLAlchemy database URL."""
        if not self.db_path:
            msg = (
                "DB_PATH environment variable is required but not set. "
                "Please set DB_PATH in your .env file or environment."
            )
            raise ValueError(msg)
        return f"sqlite:///{self.db_path}"

    @property
    def prisma_database_url(self) -> str:
        """Prisma database URL."""
        if not self.db_path:
            msg = (
                "DB_PATH environment variable is required but not set. "
                "Please set DB_PATH in your .env file or environment."
            )
            raise ValueError(msg)
        return f"file:{self.db_path}"


settings = Settings()

# Set DATABASE_URL environment variable for Prisma
os.environ.setdefault("DATABASE_URL", settings.prisma_database_url)
