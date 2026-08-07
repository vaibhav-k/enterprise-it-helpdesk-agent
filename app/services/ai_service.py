"""
AI service abstraction.

This module provides a provider-independent interface
for generating AI responses.

The initial implementation uses a placeholder response.
Azure OpenAI integration will replace the implementation
without changing the application architecture.
"""

from app.core.logging import (
    get_logger,
)

logger = get_logger(
    "ai_service",
)


class AIService:
    """
    Service responsible for AI response generation.
    """

    def generate_response(
        self,
        prompt: str,
    ) -> str:
        """
        Generate an AI response.

        Args:
            prompt:
                User input or generated prompt.

        Returns:
            Generated response text.
        """

        logger.info(
            "ai_request_received length=%s",
            len(prompt),
        )

        response = (
            "I received your request. "
            "The AI response service is ready "
            "for Azure OpenAI integration."
        )

        logger.info(
            "ai_response_generated",
        )

        return response
