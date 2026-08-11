"""
Azure OpenAI service.

Provides the application-level interface for communicating with
Azure OpenAI using Microsoft Entra workload authentication through
DefaultAzureCredential.

An API key fallback is supported for local development only, for
cases where a developer is blocked on an RBAC grant. See
``Settings.azure_openai_api_key``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Final

from azure.identity import (
    DefaultAzureCredential,
    get_bearer_token_provider,
)
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from app.core.config import settings
from app.models.chat import ChatMessage

AZURE_OPENAI_SCOPE: Final[str] = "https://ai.azure.com/.default"


class AIService:
    """Application service for Azure OpenAI requests."""

    def __init__(self) -> None:
        """Initialize the Azure OpenAI client."""

        endpoint = settings.azure_openai_endpoint.strip()
        deployment = settings.azure_openai_deployment.strip()

        if not endpoint:
            raise ValueError(
                "AZURE_OPENAI_ENDPOINT must be configured.",
            )

        if not deployment:
            raise ValueError(
                "AZURE_OPENAI_DEPLOYMENT must be configured.",
            )

        api_key = settings.azure_openai_api_key.strip()

        # Keyless Microsoft Entra ID auth is the supported path. The
        # API key is only used as a local-development fallback when
        # explicitly configured (see Settings.azure_openai_api_key).
        api_credential: str | Callable[[], str] = (
            api_key or self._build_token_provider()
        )

        self._client = OpenAI(
            base_url=self._build_base_url(endpoint),
            api_key=api_credential,
            timeout=settings.azure_openai_timeout_seconds,
        )

        self._deployment = deployment

    @staticmethod
    def _build_token_provider() -> Callable[[], str]:
        """
        Build a Microsoft Entra ID bearer token provider.

        Returns:
            Callable token provider accepted by the OpenAI client's
            ``api_key`` parameter.
        """

        credential = DefaultAzureCredential()

        return get_bearer_token_provider(
            credential,
            AZURE_OPENAI_SCOPE,
        )

    @staticmethod
    def _build_base_url(endpoint: str) -> str:
        """
        Build the Azure OpenAI v1 API base URL.

        Args:
            endpoint: Azure OpenAI resource endpoint.

        Returns:
            Normalized Azure OpenAI v1 base URL.
        """

        normalized = endpoint.rstrip("/")

        if normalized.endswith("/openai/v1"):
            return f"{normalized}/"

        return f"{normalized}/openai/v1/"

    @staticmethod
    def _build_messages(
        messages: list[ChatMessage],
    ) -> list[
        ChatCompletionSystemMessageParam
        | ChatCompletionUserMessageParam
        | ChatCompletionAssistantMessageParam
    ]:
        """
        Convert application chat messages to OpenAI message types.

        Args:
            messages: Application-level chat messages.

        Returns:
            OpenAI-compatible typed chat messages.

        Raises:
            ValueError: If an unsupported role is provided.
        """

        openai_messages: list[
            ChatCompletionSystemMessageParam
            | ChatCompletionUserMessageParam
            | ChatCompletionAssistantMessageParam
        ] = []

        for message in messages:
            if message.role == "system":
                openai_messages.append(
                    ChatCompletionSystemMessageParam(
                        role="system",
                        content=message.content,
                    ),
                )
            elif message.role == "user":
                openai_messages.append(
                    ChatCompletionUserMessageParam(
                        role="user",
                        content=message.content,
                    ),
                )
            elif message.role == "assistant":
                openai_messages.append(
                    ChatCompletionAssistantMessageParam(
                        role="assistant",
                        content=message.content,
                    ),
                )
            else:
                raise ValueError(
                    f"Unsupported chat role: {message.role}",
                )

        return openai_messages

    def generate_response(
        self,
        messages: list[ChatMessage],
    ) -> str:
        """
        Generate an Azure OpenAI response.

        Args:
            messages: Application-level conversation messages.

        Returns:
            Generated assistant response.

        Raises:
            RuntimeError: If Azure OpenAI fails or returns no content.
            ValueError: If an unsupported message role is provided.
        """

        openai_messages = self._build_messages(messages)

        try:
            response = self._client.chat.completions.create(
                model=self._deployment,
                messages=openai_messages,
                # `max_tokens` is deprecated by Azure OpenAI in favor of
                # `max_completion_tokens`, and reasoning-family models
                # (o-series, GPT-5, etc.) reject `max_tokens` outright
                # with a 400. `max_completion_tokens` is accepted by
                # both older and newer chat-completions models.
                max_completion_tokens=settings.azure_openai_max_tokens,
            )
        except Exception as exc:
            raise RuntimeError(
                "Azure OpenAI request failed.",
            ) from exc

        if not response.choices:
            raise RuntimeError(
                "Azure OpenAI returned no response choices.",
            )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "Azure OpenAI returned an empty response.",
            )

        return content.strip()
