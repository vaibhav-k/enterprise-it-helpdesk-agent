"""
Unit tests for Azure OpenAI integration.
"""

from unittest.mock import MagicMock, patch

import pytest

from app.services.ai_service import AIService


def _create_service_patches() -> tuple[
    MagicMock,
    MagicMock,
    MagicMock,
]:
    """
    Create mocked Azure OpenAI dependencies.

    Returns:
        Tuple containing credential, token provider, and OpenAI client mocks.
    """

    credential = MagicMock()
    token_provider = MagicMock()
    openai_client = MagicMock()

    return credential, token_provider, openai_client


def test_build_base_url_public_behavior() -> None:
    """Verify Azure OpenAI base URL construction."""

    credential, token_provider, openai_client = _create_service_patches()

    with patch(
        "app.services.ai_service.settings.azure_openai_endpoint",
        "https://example.openai.azure.com",
    ), patch(
        "app.services.ai_service.settings.azure_openai_deployment",
        "helpdesk-model",
    ), patch(
        "app.services.ai_service.DefaultAzureCredential",
        return_value=credential,
    ), patch(
        "app.services.ai_service.get_bearer_token_provider",
        return_value=token_provider,
    ), patch(
        "app.services.ai_service.OpenAI",
        return_value=openai_client,
    ) as mock_openai:
        AIService()

    mock_openai.assert_called_once()

    _, kwargs = mock_openai.call_args

    assert kwargs["base_url"] == "https://example.openai.azure.com/openai/v1/"

    assert kwargs["api_key"] is token_provider


def test_build_base_url_preserves_v1_endpoint() -> None:
    """Verify an existing v1 endpoint is not duplicated."""

    credential, token_provider, openai_client = _create_service_patches()

    with patch(
        "app.services.ai_service.settings.azure_openai_endpoint",
        "https://example.openai.azure.com/openai/v1",
    ), patch(
        "app.services.ai_service.settings.azure_openai_deployment",
        "helpdesk-model",
    ), patch(
        "app.services.ai_service.DefaultAzureCredential",
        return_value=credential,
    ), patch(
        "app.services.ai_service.get_bearer_token_provider",
        return_value=token_provider,
    ), patch(
        "app.services.ai_service.OpenAI",
        return_value=openai_client,
    ) as mock_openai:
        AIService()

    _, kwargs = mock_openai.call_args

    assert kwargs["base_url"] == "https://example.openai.azure.com/openai/v1/"


def test_requires_endpoint() -> None:
    """Verify Azure OpenAI endpoint configuration is required."""

    with patch(
        "app.services.ai_service.settings.azure_openai_endpoint",
        "",
    ):
        with pytest.raises(
            ValueError,
            match="AZURE_OPENAI_ENDPOINT must be configured",
        ):
            AIService()


def test_requires_deployment() -> None:
    """Verify Azure OpenAI deployment configuration is required."""

    with patch(
        "app.services.ai_service.settings.azure_openai_endpoint",
        "https://example.openai.azure.com",
    ), patch(
        "app.services.ai_service.settings.azure_openai_deployment",
        "",
    ):
        with pytest.raises(
            ValueError,
            match="AZURE_OPENAI_DEPLOYMENT must be configured",
        ):
            AIService()


def test_generate_response() -> None:
    """Verify Azure OpenAI response extraction."""

    credential, token_provider, openai_client = _create_service_patches()

    response = MagicMock()
    response.choices = [
        MagicMock(
            message=MagicMock(
                content="  Test AI response.  ",
            ),
        ),
    ]

    openai_client.chat.completions.create.return_value = response

    with patch(
        "app.services.ai_service.settings.azure_openai_endpoint",
        "https://example.openai.azure.com",
    ), patch(
        "app.services.ai_service.settings.azure_openai_deployment",
        "helpdesk-model",
    ), patch(
        "app.services.ai_service.DefaultAzureCredential",
        return_value=credential,
    ), patch(
        "app.services.ai_service.get_bearer_token_provider",
        return_value=token_provider,
    ), patch(
        "app.services.ai_service.OpenAI",
        return_value=openai_client,
    ):
        service = AIService()

        result = service.generate_response(
            [
                {
                    "role": "user",
                    "content": "How do I reset my password?",
                },
            ],
        )

    assert result == "Test AI response."

    openai_client.chat.completions.create.assert_called_once()


def test_generate_response_requires_choices() -> None:
    """Verify an empty Azure OpenAI response is rejected."""

    credential, token_provider, openai_client = _create_service_patches()

    response = MagicMock()
    response.choices = []

    openai_client.chat.completions.create.return_value = response

    with patch(
        "app.services.ai_service.settings.azure_openai_endpoint",
        "https://example.openai.azure.com",
    ), patch(
        "app.services.ai_service.settings.azure_openai_deployment",
        "helpdesk-model",
    ), patch(
        "app.services.ai_service.DefaultAzureCredential",
        return_value=credential,
    ), patch(
        "app.services.ai_service.get_bearer_token_provider",
        return_value=token_provider,
    ), patch(
        "app.services.ai_service.OpenAI",
        return_value=openai_client,
    ):
        service = AIService()

        with pytest.raises(
            RuntimeError,
            match="Azure OpenAI returned no response choices",
        ):
            service.generate_response(
                [
                    {
                        "role": "user",
                        "content": "Test",
                    },
                ],
            )


def test_generate_response_rejects_empty_content() -> None:
    """Verify an empty Azure OpenAI message is rejected."""

    credential, token_provider, openai_client = _create_service_patches()

    response = MagicMock()
    response.choices = [
        MagicMock(
            message=MagicMock(
                content=None,
            ),
        ),
    ]

    openai_client.chat.completions.create.return_value = response

    with patch(
        "app.services.ai_service.settings.azure_openai_endpoint",
        "https://example.openai.azure.com",
    ), patch(
        "app.services.ai_service.settings.azure_openai_deployment",
        "helpdesk-model",
    ), patch(
        "app.services.ai_service.DefaultAzureCredential",
        return_value=credential,
    ), patch(
        "app.services.ai_service.get_bearer_token_provider",
        return_value=token_provider,
    ), patch(
        "app.services.ai_service.OpenAI",
        return_value=openai_client,
    ):
        service = AIService()

        with pytest.raises(
            RuntimeError,
            match="Azure OpenAI returned an empty response",
        ):
            service.generate_response(
                [
                    {
                        "role": "user",
                        "content": "Test",
                    },
                ],
            )
