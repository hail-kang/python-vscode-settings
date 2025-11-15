"""Application configuration."""

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

    # API
    api_v1_prefix: str = "/api/v1"


settings = Settings()
