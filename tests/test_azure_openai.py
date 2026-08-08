"""
Azure OpenAI service tests.
"""

import pytest

from app.core.config import settings
from app.services.azure_openai_service import AzureOpenAIService


def test_azure_openai_requires_endpoint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Verify the service rejects missing Azure OpenAI configuration.
    """

    monkeypatch.setattr(
        settings,
        "azure_openai_endpoint",
        "",
    )

    monkeypatch.setattr(
        settings,
        "azure_openai_deployment",
        "test-deployment",
    )

    with pytest.raises(
        ValueError,
        match="AZURE_OPENAI_ENDPOINT",
    ):
        AzureOpenAIService()
