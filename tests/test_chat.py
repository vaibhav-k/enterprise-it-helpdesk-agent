"""
Tests for the helpdesk agent.
"""

from app.agents.helpdesk_agent import HelpdeskAgent
from app.services.ai_service import ChatMessage


class FakeAIService:
    """Fake AI service used for unit testing."""

    def generate_response(
        self,
        messages: list[ChatMessage],
    ) -> str:
        """Return a deterministic test response."""

        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "My laptop is not working."

        return "Please restart your laptop and try again."


def test_helpdesk_agent_response() -> None:
    """Verify the helpdesk agent generates a response."""

    agent = HelpdeskAgent(FakeAIService())

    response = agent.process_request(
        "My laptop is not working.",
    )

    assert response == "Please restart your laptop and try again."


def test_helpdesk_agent_rejects_empty_message() -> None:
    """Verify empty helpdesk messages are rejected."""

    agent = HelpdeskAgent(FakeAIService())

    try:
        agent.process_request("   ")
    except ValueError as exc:
        assert str(exc) == "Message must not be empty."
    else:
        raise AssertionError("Expected ValueError.")
