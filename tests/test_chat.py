"""
Chat API tests.
"""

from app.agents.helpdesk_agent import HelpdeskAgent
from app.services.ai_service import AIService


def test_helpdesk_agent_response() -> None:
    """
    Verify helpdesk agent generates response.
    """

    agent = HelpdeskAgent(AIService())

    response = agent.process_request(
        "My laptop is not connecting to WiFi",
    )

    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
