"""
Application configuration.
"""

from pydantic_settings import (
    BaseSettings,
)


class Settings(BaseSettings):
    """
    Application settings.
    """

    app_name: str = "Enterprise IT Helpdesk Agent"

    jwt_secret: str

    jwt_algorithm: str = "HS256"

    jwt_expiry_minutes: int = 480

    azure_storage_account: str

    azure_container: str = "knowledge-base"

    keyvault_name: str

    class Config:

        env_file = ".env"


settings = Settings()
