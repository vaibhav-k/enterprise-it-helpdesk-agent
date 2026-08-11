"""
Azure OpenAI service.

Provides the application-level interface for communicating with
Azure OpenAI using Microsoft Entra workload authentication through
DefaultAzureCredential.

An API key fallback is supported for local development only, for
cases where a developer is blocked on an RBAC grant. See
``Settings.azure_openai_api_key``.

Transient failures (429 rate limits, 5xx errors, timeouts, connection
errors) are retried with exponential backoff and jitter. Non-transient
failures (bad request, auth, not found) fail immediately.
"""

from __future__ import annotations

import random
import time
from collections.abc import Callable
from typing import Final

from azure.identity import (
    DefaultAzureCredential,
    get_bearer_token_provider,
)
from openai import (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    OpenAI,
    RateLimitError,
)
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionAssistantMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    CompletionCreateParams,
)

from app.core.config import settings
from app.core.logging import get_logger
from app.models.chat import ChatMessage

AZURE_OPENAI_SCOPE: Final[str] = "https://ai.azure.com/.default"

# Errors worth retrying: throttling, transient server-side failures,
# and network-level failures. Anything else (bad request, auth,
# not found) is a caller/config problem that a retry won't fix.
RETRYABLE_EXCEPTIONS: Final[tuple[type[Exception], ...]] = (
    RateLimitError,
    APITimeoutError,
    APIConnectionError,
    InternalServerError,
)

logger = get_logger("ai_service")


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
        *,
        user_identifier: str | None = None,
    ) -> str:
        """
        Generate an Azure OpenAI response.

        Args:
            messages: Application-level conversation messages.
            user_identifier: Opaque identifier for the end user making
                the request (e.g. the authenticated username). Passed
                through to Azure OpenAI's ``user`` field so that
                requests are traceable back to the human who triggered
                them, for abuse monitoring and audit purposes. This is
                identity *propagation for observability*, not
                delegated authorization: the call is still made under
                the application's own Azure identity.

        Returns:
            Generated assistant response.

        Raises:
            RuntimeError: If Azure OpenAI fails or returns no content.
            ValueError: If an unsupported message role is provided.
        """

        openai_messages = self._build_messages(messages)

        response = self._create_completion_with_retry(
            openai_messages,
            user_identifier=user_identifier,
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

    def _create_completion_with_retry(
        self,
        openai_messages: list[
            ChatCompletionSystemMessageParam
            | ChatCompletionUserMessageParam
            | ChatCompletionAssistantMessageParam
        ],
        *,
        user_identifier: str | None,
    ) -> ChatCompletion:
        """
        Call Azure OpenAI, retrying transient failures with backoff.

        Retries on rate limits, transient server errors, timeouts, and
        connection errors, up to ``settings.azure_openai_max_retries``
        additional attempts. Every other failure (bad request, auth,
        not found, an unsupported message role, ...) is raised
        immediately without retrying.

        Args:
            openai_messages: OpenAI-compatible chat messages.
            user_identifier: Opaque end-user identifier, if any.

        Returns:
            The Azure OpenAI chat completion response.

        Raises:
            RuntimeError: If every attempt fails, or a non-retryable
                error occurs.
        """

        max_attempts = settings.azure_openai_max_retries + 1
        request_kwargs: CompletionCreateParams = {
            "model": self._deployment,
            "messages": openai_messages,
            # `max_tokens` is deprecated by Azure OpenAI in favor of
            # `max_completion_tokens`, and reasoning-family models
            # (o-series, GPT-5, etc.) reject `max_tokens` outright
            # with a 400. `max_completion_tokens` is accepted by
            # both older and newer chat-completions models.
            "max_completion_tokens": settings.azure_openai_max_tokens,
        }

        if user_identifier:
            request_kwargs["user"] = user_identifier[:64]

        logger.info(
            "azure_openai_request user=%s",
            request_kwargs.get("user", "(none)"),
        )

        last_error: Exception | None = None

        for attempt in range(1, max_attempts + 1):
            try:
                return self._client.chat.completions.create(
                    **request_kwargs,
                )
            except RETRYABLE_EXCEPTIONS as exc:
                last_error = exc

                if attempt >= max_attempts:
                    break

                delay = self._compute_backoff_seconds(attempt, exc)

                logger.warning(
                    "azure_openai_retry attempt=%s/%s error=%s delay=%.2f",
                    attempt,
                    max_attempts,
                    exc.__class__.__name__,
                    delay,
                )

                time.sleep(delay)
            except Exception as exc:
                # Non-retryable: bad request, auth, not found, etc.
                raise RuntimeError(
                    "Azure OpenAI request failed.",
                ) from exc

        raise RuntimeError(
            "Azure OpenAI request failed after retrying.",
        ) from last_error

    @staticmethod
    def _compute_backoff_seconds(
        attempt: int,
        exc: Exception,
    ) -> float:
        """
        Compute the delay before the next retry attempt.

        Honors a server-provided ``Retry-After`` header when present
        (as Azure OpenAI sends on 429 responses); otherwise falls back
        to exponential backoff with jitter.

        Args:
            attempt: The attempt number that just failed (1-indexed).
            exc: The exception raised by the failed attempt.

        Returns:
            Delay in seconds before the next attempt.
        """

        retry_after = getattr(exc, "response", None)

        if retry_after is not None:
            header_value = retry_after.headers.get("retry-after")

            if header_value is not None:
                try:
                    return max(float(header_value), 0.0)
                except ValueError:
                    pass

        base = settings.azure_openai_retry_base_seconds
        capped = min(
            base * (2 ** (attempt - 1)),
            settings.azure_openai_retry_max_seconds,
        )

        # Full jitter: uniformly random in [0, capped]. Avoids every
        # concurrent request retrying in lockstep.
        return random.uniform(0.0, capped)
