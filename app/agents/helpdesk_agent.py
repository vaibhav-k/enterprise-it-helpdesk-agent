"""
Enterprise IT helpdesk agent.
"""

from typing import Protocol

from app.models.chat import ChatMessage, ChatRequest


class AIServiceProtocol(Protocol):
    """Protocol implemented by AI providers."""

    def generate_response(
        self,
        messages: list[ChatMessage],
    ) -> str:
        """
        Generate an AI response.

        Args:
            messages: Conversation messages.

        Returns:
            Generated response.
        """

        ...


class HelpdeskAgent:
    """Application-level helpdesk agent."""

    def __init__(
        self,
        ai_service: AIServiceProtocol,
    ) -> None:
        """
        Initialize the helpdesk agent.

        Args:
            ai_service: AI provider implementation.
        """

        self._ai_service = ai_service

    def process_request(
        self,
        request: ChatRequest,
    ) -> str:
        """
        Process a helpdesk request with conversation context.

        Args:
            request: Chat request containing the current message
            and optional conversation history.

        Returns:
            Generated helpdesk response.
        """

        messages: list[ChatMessage] = [
            *request.history,
            ChatMessage(
                role="user",
                content=request.message,
            ),
        ]

        return self._ai_service.generate_response(messages)
