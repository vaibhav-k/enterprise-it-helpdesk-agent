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

    # Optional local-development fallback. Leave unset in every shared
    # or production environment: Microsoft Entra ID / managed identity
    # (DefaultAzureCredential) is the supported enterprise auth path.
    # This exists only so a developer who is blocked on an RBAC grant
    # for "Cognitive Services OpenAI User" can keep working locally
    # using a key someone with resource access hands them.
    azure_openai_api_key: str = ""

    knowledge_max_documents: int = 5
    knowledge_max_document_chars: int = 12_000
    knowledge_max_context_chars: int = 40_000

    # Retry / backoff for transient Azure OpenAI failures (429, 5xx,
    # timeouts, connection errors). Total worst-case attempts is
    # 1 + azure_openai_max_retries.
    azure_openai_max_retries: int = 3
    azure_openai_retry_base_seconds: float = 0.5
    azure_openai_retry_max_seconds: float = 8.0

    # Rate limiting (in-memory, per-process). See app/core/rate_limit.py.
    # Suitable for a single-instance deployment; a multi-instance
    # deployment needs a shared store (e.g. Redis) instead.
    rate_limit_login_max_requests: int = 5
    rate_limit_login_window_seconds: float = 60.0
    rate_limit_chat_max_requests: int = 20
    rate_limit_chat_window_seconds: float = 60.0

    # Session persistence (in-memory, per-process; see
    # app/database/sessions.py). Bounds how much conversation history
    # is retained server-side per chat session.
    session_max_messages: int = 20
    session_max_per_user: int = 20

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
