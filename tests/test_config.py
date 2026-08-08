"""
Configuration tests.
"""

from app.core.config import settings


def test_azure_openai_timeout_default() -> None:
    """Verify the default Azure OpenAI timeout."""

    assert settings.azure_openai_timeout_seconds == 30.0


def test_settings_load() -> None:
    """
    Verify application settings load correctly.
    """

    assert settings.app_name == "Enterprise IT Helpdesk Agent"
    assert settings.environment == "development"
