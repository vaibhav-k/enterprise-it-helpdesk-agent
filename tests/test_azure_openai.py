"""
Unit tests for Azure OpenAI integration.

All Azure OpenAI interactions are mocked. These tests never contact Azure.
"""

from unittest.mock import MagicMock, patch

import pytest

from app.services.ai_service import AIService

ENDPOINT = "https://example.openai.azure.com"
DEPLOYMENT = "helpdesk-model"


def create_service_mocks() -> tuple[
    MagicMock,
    MagicMock,
    MagicMock,
]:
    """
    Create mocked Azure OpenAI dependencies.

    Returns:
        Credential, token provider, and OpenAI client mocks.
    """

    credential = MagicMock()
    token_provider = MagicMock()
    openai_client = MagicMock()

    return credential, token_provider, openai_client


def create_service(
    openai_client: MagicMock,
    token_provider: MagicMock,
    credential: MagicMock,
) -> AIService:
    """
    Create an AIService with Azure dependencies mocked.

    Args:
        openai_client: Mocked OpenAI client.
        token_provider: Mocked bearer token provider.
        credential: Mocked Azure credential.

    Returns:
        Configured AIService instance.
    """

    with patch(
        "app.services.ai_service.settings.azure_openai_endpoint",
        ENDPOINT,
    ), patch(
        "app.services.ai_service.settings.azure_openai_deployment",
        DEPLOYMENT,
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
        return AIService()


def test_missing_endpoint() -> None:
    """Verify the Azure OpenAI endpoint is required."""

    with patch(
        "app.services.ai_service.settings.azure_openai_endpoint",
        "",
    ), patch(
        "app.services.ai_service.settings.azure_openai_deployment",
        DEPLOYMENT,
    ):
        with pytest.raises(
            ValueError,
            match="AZURE_OPENAI_ENDPOINT must be configured",
        ):
            AIService()


def test_missing_deployment() -> None:
    """Verify the Azure OpenAI deployment is required."""

    with patch(
        "app.services.ai_service.settings.azure_openai_endpoint",
        ENDPOINT,
    ), patch(
        "app.services.ai_service.settings.azure_openai_deployment",
        "",
    ):
        with pytest.raises(
            ValueError,
            match="AZURE_OPENAI_DEPLOYMENT must be configured",
        ):
            AIService()


def test_successful_response() -> None:
    """Verify a successful Azure OpenAI response is returned."""

    credential, token_provider, openai_client = create_service_mocks()

    response = MagicMock()
    response.choices = [
        MagicMock(
            message=MagicMock(
                content="  Test AI response.  ",
            ),
        ),
    ]

    openai_client.chat.completions.create.return_value = response

    service = create_service(
        openai_client,
        token_provider,
        credential,
    )

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


def test_empty_response() -> None:
    """Verify an empty Azure OpenAI response is rejected."""

    credential, token_provider, openai_client = create_service_mocks()

    response = MagicMock()
    response.choices = []

    openai_client.chat.completions.create.return_value = response

    service = create_service(
        openai_client,
        token_provider,
        credential,
    )

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


def test_azure_openai_failure() -> None:
    """Verify provider failures are converted to RuntimeError."""

    credential, token_provider, openai_client = create_service_mocks()

    openai_client.chat.completions.create.side_effect = RuntimeError(
        "simulated Azure OpenAI failure"
    )

    service = create_service(
        openai_client,
        token_provider,
        credential,
    )

    with pytest.raises(
        RuntimeError,
        match="Azure OpenAI request failed",
    ):
        service.generate_response(
            [
                {
                    "role": "user",
                    "content": "Test",
                },
            ],
        )


def test_timeout_configuration() -> None:
    """Verify the configured timeout is passed to the OpenAI client."""

    credential, token_provider, openai_client = create_service_mocks()

    with patch(
        "app.services.ai_service.settings.azure_openai_endpoint",
        ENDPOINT,
    ), patch(
        "app.services.ai_service.settings.azure_openai_deployment",
        DEPLOYMENT,
    ), patch(
        "app.services.ai_service.settings.azure_openai_timeout_seconds",
        45.0,
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

    assert kwargs["timeout"] == 45.0


def test_empty_message_content() -> None:
    """Verify an empty AI response content is rejected."""

    credential, token_provider, openai_client = create_service_mocks()

    response = MagicMock()
    response.choices = [
        MagicMock(
            message=MagicMock(
                content=None,
            ),
        ),
    ]

    openai_client.chat.completions.create.return_value = response

    service = create_service(
        openai_client,
        token_provider,
        credential,
    )

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
