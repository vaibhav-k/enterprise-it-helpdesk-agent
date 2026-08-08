"""
Helpdesk agent orchestration.
"""

from __future__ import annotations

from typing import Protocol

from app.services.ai_service import ChatMessage


class AIServiceProtocol(Protocol):
    """Interface required by the helpdesk agent."""

    def generate_response(
        self,
        messages: list[ChatMessage],
    ) -> str:
        """Generate an AI response from chat messages."""
        ...


class HelpdeskAgent:
    """Application-level helpdesk agent."""

    def __init__(self, ai_service: AIServiceProtocol) -> None:
        """
        Initialize the helpdesk agent.

        Args:
            ai_service: AI provider implementing the required interface.
        """

        self._ai_service = ai_service

    def process_request(self, message: str) -> str:
        """
        Process a helpdesk request.

        Args:
            message: User's helpdesk message.

        Returns:
            Generated assistant response.

        Raises:
            ValueError: If the message is empty.
        """

        cleaned_message = message.strip()

        if not cleaned_message:
            raise ValueError("Message must not be empty.")

        messages: list[ChatMessage] = [
            {
                "role": "system",
                "content": (
                    "You are an enterprise IT helpdesk assistant. "
                    "Provide clear, concise, and safe IT support guidance. "
                    "Do not invent company policies, credentials, or "
                    "security-sensitive information."
                ),
            },
            {
                "role": "user",
                "content": cleaned_message,
            },
        ]

        return self._ai_service.generate_response(messages)
