from app.core.config import Settings

settings = Settings()

assert settings.app_name == "Enterprise IT Helpdesk Agent"
assert settings.jwt_algorithm == "HS256"
