"""
Enterprise IT Helpdesk Agent.

Responsible for coordinating user requests
and generating support responses.

The agent delegates AI generation to AIService.
"""

from app.core.logging import (
    get_logger,
)
from app.services.ai_service import (
    AIService,
)

logger = get_logger(
    "helpdesk_agent",
)


class HelpdeskAgent:
    """
    Main helpdesk agent orchestrator.
    """

    def __init__(
        self,
        ai_service: AIService,
    ) -> None:
        """
        Initialize helpdesk agent.

        Args:
            ai_service:
                AI response generation service.
        """

        self.ai_service = ai_service

    def process_request(
        self,
        message: str,
    ) -> str:
        """
        Process employee helpdesk request.

        Args:
            message:
                Employee question.

        Returns:
            Generated helpdesk response.
        """

        logger.info(
            "helpdesk_request_received",
        )

        prompt = self._build_prompt(
            message,
        )

        response = self.ai_service.generate_response(prompt)

        logger.info(
            "helpdesk_response_completed",
        )

        return response

    def _build_prompt(
        self,
        message: str,
    ) -> str:
        """
        Build AI prompt.

        Args:
            message:
                Employee question.

        Returns:
            Formatted AI prompt.
        """

        return (
            "You are an enterprise IT helpdesk assistant.\n\n"
            "Help the employee with the following request:\n\n"
            f"{message}"
        )
