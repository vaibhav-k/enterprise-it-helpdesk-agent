"""
Configuration tests.
"""

from app.core.config import settings


def test_settings_load() -> None:
    """
    Verify application settings load correctly.
    """

    assert settings.app_name == "Enterprise IT Helpdesk Agent"
    assert settings.environment == "development"
