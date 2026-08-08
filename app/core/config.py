"""
Application configuration.

Loads application settings from environment variables
and optional .env configuration.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "Enterprise IT Helpdesk Agent"
    environment: str = "development"

    enable_audit_logging: bool = True

    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expiry_minutes: int = 480

    azure_storage_account: str = ""
    azure_container: str = "knowledge-base"

    keyvault_name: str = ""

    azure_openai_endpoint: str = ""
    azure_openai_api_version: str = "2024-10-21"
    azure_openai_deployment: str = ""
    azure_openai_timeout_seconds: float = 30.0
    azure_openai_max_tokens: int = 800

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    if not azure_openai_endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT must be configured.")

    if not azure_openai_deployment:
        raise ValueError("AZURE_OPENAI_DEPLOYMENT must be configured.")


settings = Settings()
