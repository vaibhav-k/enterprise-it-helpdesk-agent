"""
Azure identity tests.
"""

from unittest.mock import MagicMock, patch

from azure.identity import DefaultAzureCredential

from app.core.azure_identity import (
    get_azure_credential,
)
from app.models.chat import ChatMessage
from app.services.ai_service import AIService


def test_azure_credential_type() -> None:
    """
    Verify Azure credential factory.
    """

    credential = get_azure_credential()

    assert isinstance(
        credential,
        DefaultAzureCredential,
    )


def test_generate_response_supports_system_message() -> None:
    """Verify system messages are accepted by the public API."""

    messages = [
        ChatMessage(
            role="system",
            content="Use enterprise documentation.",
        ),
        ChatMessage(
            role="user",
            content="How do I reset my password?",
        ),
    ]

    with patch(
        "app.services.ai_service.settings.azure_openai_endpoint",
        "https://example.openai.azure.com",
    ):
        with patch(
            "app.services.ai_service.settings.azure_openai_deployment",
            "helpdesk-model",
        ):
            with patch(
                "app.services.ai_service.DefaultAzureCredential",
            ):
                with patch(
                    "app.services.ai_service.get_bearer_token_provider",
                    return_value="token-provider",
                ):
                    with patch(
                        "app.services.ai_service.OpenAI",
                    ) as mock_openai:
                        mock_client = mock_openai.return_value

                        mock_client.chat.completions.create.return_value = MagicMock(
                            choices=[
                                MagicMock(
                                    message=MagicMock(
                                        content="Use the VPN reset guide.",
                                    ),
                                ),
                            ],
                        )

                        service = AIService()

                        result = service.generate_response(
                            messages,
                        )

    assert result == "Use the VPN reset guide."

    create_call = mock_client.chat.completions.create.call_args

    assert create_call is not None

    sent_messages = create_call.kwargs["messages"]

    assert sent_messages[0]["role"] == "system"
    assert sent_messages[0]["content"] == ("Use enterprise documentation.")

    assert sent_messages[1]["role"] == "user"
    assert sent_messages[1]["content"] == ("How do I reset my password?")
