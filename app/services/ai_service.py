"""
Azure OpenAI service.

Provides the application-level interface for communicating with
Azure OpenAI using Microsoft Entra workload authentication through
DefaultAzureCredential.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from app.core.config import settings

AZURE_OPENAI_SCOPE: Final[str] = "https://ai.azure.com/.default"

# Public type alias used by the agent layer.
ChatMessage = ChatCompletionMessageParam


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

        credential = DefaultAzureCredential()

        token_provider = get_bearer_token_provider(
            credential,
            AZURE_OPENAI_SCOPE,
        )

        self._client = OpenAI(
            base_url=self._build_base_url(endpoint),
            api_key=token_provider,
        )

        self._deployment = deployment

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

    def generate_response(
        self,
        messages: Sequence[ChatMessage],
    ) -> str:
        """
        Generate an assistant response.

        Args:
            messages: Conversation messages sent to Azure OpenAI.

        Returns:
            Generated assistant response.

        Raises:
            RuntimeError: If Azure OpenAI returns no usable response.
        """

        response = self._client.chat.completions.create(
            model=self._deployment,
            messages=list(messages),
        )

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
