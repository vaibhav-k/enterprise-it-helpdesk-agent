from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "Enterprise IT Helpdesk Agent"

    jwt_secret: str

    jwt_algorithm: str = "HS256"

    jwt_expiry_minutes: int = 480

    azure_storage_account: str

    azure_container: str

    keyvault_name: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
