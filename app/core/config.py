"""
Application configuration.

Loads application settings from environment variables
and optional .env configuration.
"""

from pydantic import model_validator
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

    knowledge_max_documents: int = 5
    knowledge_max_document_chars: int = 12_000
    knowledge_max_context_chars: int = 40_000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @model_validator(mode="after")
    def _validate_required_settings(self) -> "Settings":
        """
        Validate settings after environment values have been loaded.

        The previous implementation checked the class-body default
        values (always empty strings) instead of the values actually
        loaded from the environment, so this validation unconditionally
        raised on import regardless of configuration. Validating the
        instance in a model validator ensures real, loaded values are
        checked instead.
        """

        if not self.azure_openai_endpoint.strip():
            raise ValueError("AZURE_OPENAI_ENDPOINT must be configured.")

        if not self.azure_openai_deployment.strip():
            raise ValueError("AZURE_OPENAI_DEPLOYMENT must be configured.")

        if not self.jwt_secret.strip():
            raise ValueError("JWT_SECRET must be configured.")

        return self


settings = Settings()
