"""
Application configuration.

Loads application settings from environment variables
and optional .env configuration.
"""

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """
    Application settings.

    Values can be overridden using environment variables
    or a local .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

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

    azure_openai_deployment: str = ""

    azure_openai_api_version: str = ""

    azure_openai_enabled: bool = False


settings = Settings()
