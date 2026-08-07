"""
Application configuration module.

Loads application settings from environment variables
using Pydantic Settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application runtime configuration.
    """

    app_name: str = "Enterprise IT Helpdesk Agent"

    jwt_secret: str

    jwt_algorithm: str = "HS256"

    jwt_expiry_minutes: int = 480

    azure_storage_account: str

    azure_container: str = "knowledge-base"

    keyvault_name: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
