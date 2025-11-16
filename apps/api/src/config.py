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

    # Database - DB_PATH is required and must be set via environment variable
    db_path: str

    # API
    api_v1_prefix: str = "/api/v1"

    @property
    def database_url(self) -> str:
        """SQLAlchemy database URL."""
        return f"sqlite:///{self.db_path}"

    @property
    def prisma_database_url(self) -> str:
        """Prisma database URL."""
        return f"file:{self.db_path}"


settings = Settings()  # type: ignore[call-arg]

# Set DATABASE_URL environment variable for Prisma
os.environ.setdefault("DATABASE_URL", settings.prisma_database_url)
