"""
Unit tests for Azure OpenAI integration.

All Azure OpenAI interactions are mocked. These tests never contact Azure.
"""

from unittest.mock import MagicMock, patch

import httpx
import pytest
from openai import APIConnectionError, RateLimitError

from app.models.chat import ChatMessage
from app.services.ai_service import AIService

ENDPOINT = "https://example.openai.azure.com"
DEPLOYMENT = "helpdesk-model"


def make_rate_limit_error(retry_after: str | None = None) -> RateLimitError:
    """
    Build a ``RateLimitError`` as Azure OpenAI would raise it on a 429.

    Args:
        retry_after: Optional ``Retry-After`` header value to attach.

    Returns:
        A populated ``RateLimitError``.
    """

    headers = {"retry-after": retry_after} if retry_after else {}

    response = httpx.Response(
        status_code=429,
        headers=headers,
        request=httpx.Request("POST", ENDPOINT),
    )

    return RateLimitError("Rate limit exceeded", response=response, body=None)


def make_connection_error() -> APIConnectionError:
    """Build an ``APIConnectionError`` as raised on a network failure."""

    return APIConnectionError(request=httpx.Request("POST", ENDPOINT))


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

    with (
        patch(
            "app.services.ai_service.settings.azure_openai_endpoint",
            ENDPOINT,
        ),
        patch(
            "app.services.ai_service.settings.azure_openai_deployment",
            DEPLOYMENT,
        ),
        patch(
            "app.services.ai_service.DefaultAzureCredential",
            return_value=credential,
        ),
        patch(
            "app.services.ai_service.get_bearer_token_provider",
            return_value=token_provider,
        ),
        patch(
            "app.services.ai_service.OpenAI",
            return_value=openai_client,
        ),
    ):
        return AIService()


def test_missing_endpoint() -> None:
    """Verify the Azure OpenAI endpoint is required."""

    with (
        patch(
            "app.services.ai_service.settings.azure_openai_endpoint",
            "",
        ),
        patch(
            "app.services.ai_service.settings.azure_openai_deployment",
            DEPLOYMENT,
        ),
    ):
        with pytest.raises(
            ValueError,
            match="AZURE_OPENAI_ENDPOINT must be configured",
        ):
            AIService()


def test_missing_deployment() -> None:
    """Verify the Azure OpenAI deployment is required."""

    with (
        patch(
            "app.services.ai_service.settings.azure_openai_endpoint",
            ENDPOINT,
        ),
        patch(
            "app.services.ai_service.settings.azure_openai_deployment",
            "",
        ),
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
            ChatMessage(
                role="user",
                content="How do I reset my password?",
            ),
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

    messages = [
        ChatMessage(
            role="user",
            content="Test",
        ),
    ]

    with pytest.raises(
        RuntimeError,
        match="Azure OpenAI returned no response choices",
    ):
        service.generate_response(messages)


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

    messages = [
        ChatMessage(
            role="user",
            content="Test",
        ),
    ]

    with pytest.raises(
        RuntimeError,
        match="Azure OpenAI request failed",
    ):
        service.generate_response(messages)


def test_timeout_configuration() -> None:
    """Verify the configured timeout is passed to the OpenAI client."""

    credential, token_provider, openai_client = create_service_mocks()

    with (
        patch(
            "app.services.ai_service.settings.azure_openai_endpoint",
            ENDPOINT,
        ),
        patch(
            "app.services.ai_service.settings.azure_openai_deployment",
            DEPLOYMENT,
        ),
        patch(
            "app.services.ai_service.settings.azure_openai_timeout_seconds",
            45.0,
        ),
        patch(
            "app.services.ai_service.DefaultAzureCredential",
            return_value=credential,
        ),
        patch(
            "app.services.ai_service.get_bearer_token_provider",
            return_value=token_provider,
        ),
        patch(
            "app.services.ai_service.OpenAI",
            return_value=openai_client,
        ) as mock_openai,
    ):
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

    messages = [
        ChatMessage(
            role="user",
            content="Test",
        ),
    ]

    with pytest.raises(
        RuntimeError,
        match="Azure OpenAI returned an empty response",
    ):
        service.generate_response(messages)


def test_generate_response_preserves_conversation_order() -> None:
    """Verify conversation messages are sent in order."""

    credential, token_provider, openai_client = create_service_mocks()

    response = MagicMock()
    response.choices = [
        MagicMock(
            message=MagicMock(
                content="Response",
            ),
        ),
    ]

    openai_client.chat.completions.create.return_value = response

    service = create_service(
        openai_client,
        token_provider,
        credential,
    )

    service.generate_response(
        [
            ChatMessage(
                role="user",
                content="VPN is broken.",
            ),
            ChatMessage(
                role="assistant",
                content="Let's troubleshoot it.",
            ),
            ChatMessage(
                role="user",
                content="What next?",
            ),
        ],
    )

    _, kwargs = openai_client.chat.completions.create.call_args

    messages = kwargs["messages"]

    assert [message["role"] for message in messages] == [
        "user",
        "assistant",
        "user",
    ]

    assert [message["content"] for message in messages] == [
        "VPN is broken.",
        "Let's troubleshoot it.",
        "What next?",
    ]


def test_retries_on_rate_limit_then_succeeds() -> None:
    """Verify a transient rate limit is retried and then succeeds."""

    credential, token_provider, openai_client = create_service_mocks()

    response = MagicMock()
    response.choices = [
        MagicMock(message=MagicMock(content="Recovered response.")),
    ]

    openai_client.chat.completions.create.side_effect = [
        make_rate_limit_error(),
        make_rate_limit_error(),
        response,
    ]

    service = create_service(openai_client, token_provider, credential)

    with patch("app.services.ai_service.time.sleep") as mock_sleep:
        result = service.generate_response(
            [ChatMessage(role="user", content="Test")],
        )

    assert result == "Recovered response."
    assert openai_client.chat.completions.create.call_count == 3
    assert mock_sleep.call_count == 2


def test_retries_exhausted_raises_runtime_error() -> None:
    """Verify persistent transient failures raise RuntimeError after retrying."""

    credential, token_provider, openai_client = create_service_mocks()

    openai_client.chat.completions.create.side_effect = make_connection_error()

    service = create_service(openai_client, token_provider, credential)

    with (
        patch(
            "app.services.ai_service.settings.azure_openai_max_retries",
            2,
        ),
        patch("app.services.ai_service.time.sleep") as mock_sleep,
    ):
        with pytest.raises(
            RuntimeError,
            match="Azure OpenAI request failed after retrying",
        ):
            service.generate_response(
                [ChatMessage(role="user", content="Test")],
            )

    # 1 initial attempt + 2 retries = 3 total calls, 2 sleeps in between.
    assert openai_client.chat.completions.create.call_count == 3
    assert mock_sleep.call_count == 2


def test_non_retryable_error_fails_without_retrying() -> None:
    """Verify a non-transient error is not retried."""

    credential, token_provider, openai_client = create_service_mocks()

    openai_client.chat.completions.create.side_effect = ValueError(
        "not a transient error",
    )

    service = create_service(openai_client, token_provider, credential)

    with patch("app.services.ai_service.time.sleep") as mock_sleep:
        with pytest.raises(RuntimeError, match="Azure OpenAI request failed"):
            service.generate_response(
                [ChatMessage(role="user", content="Test")],
            )

    assert openai_client.chat.completions.create.call_count == 1
    mock_sleep.assert_not_called()


def test_retry_honors_retry_after_header() -> None:
    """Verify a Retry-After header is used verbatim as the backoff delay."""

    credential, token_provider, openai_client = create_service_mocks()

    response = MagicMock()
    response.choices = [MagicMock(message=MagicMock(content="ok"))]

    openai_client.chat.completions.create.side_effect = [
        make_rate_limit_error(retry_after="3"),
        response,
    ]

    service = create_service(openai_client, token_provider, credential)

    with patch("app.services.ai_service.time.sleep") as mock_sleep:
        service.generate_response([ChatMessage(role="user", content="Test")])

    mock_sleep.assert_called_once_with(3.0)


def test_user_identifier_propagated_to_request() -> None:
    """Verify the authenticated user identifier reaches the Azure request."""

    credential, token_provider, openai_client = create_service_mocks()

    response = MagicMock()
    response.choices = [MagicMock(message=MagicMock(content="ok"))]

    openai_client.chat.completions.create.return_value = response

    service = create_service(openai_client, token_provider, credential)

    service.generate_response(
        [ChatMessage(role="user", content="Test")],
        user_identifier="employee",
    )

    _, kwargs = openai_client.chat.completions.create.call_args

    assert kwargs["user"] == "employee"


def test_user_identifier_omitted_when_not_provided() -> None:
    """Verify no ``user`` field is sent when no identifier is supplied."""

    credential, token_provider, openai_client = create_service_mocks()

    response = MagicMock()
    response.choices = [MagicMock(message=MagicMock(content="ok"))]

    openai_client.chat.completions.create.return_value = response

    service = create_service(openai_client, token_provider, credential)

    service.generate_response([ChatMessage(role="user", content="Test")])

    _, kwargs = openai_client.chat.completions.create.call_args

    assert "user" not in kwargs
