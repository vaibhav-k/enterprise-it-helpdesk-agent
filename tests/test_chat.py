"""
Tests for the helpdesk chat API.
"""

from typing import cast

import httpx2
from fastapi.testclient import TestClient

from app.agents.helpdesk_agent import HelpdeskAgent
from app.api.chat import get_helpdesk_agent
from app.core.security import get_current_user
from app.main import app
from app.models.chat import ChatMessage, ChatRequest


class FakeHelpdeskAgent:
    """Fake helpdesk agent for API tests."""

    def process_request(self, message: str) -> str:
        """
        Return a deterministic response.

        Args:
            message: User's helpdesk message.

        Returns:
            Fake helpdesk response.
        """

        return f"Test response: {message}"


def test_chat_endpoint() -> None:
    """Verify the chat endpoint delegates to the helpdesk agent."""

    def fake_current_user() -> dict[str, str]:
        """Return a test employee identity."""

        return {
            "username": "employee",
            "role": "employee",
        }

    def fake_helpdesk_agent() -> FakeHelpdeskAgent:
        """Return the fake helpdesk agent."""

        return FakeHelpdeskAgent()

    app.dependency_overrides[get_current_user] = fake_current_user
    app.dependency_overrides[get_helpdesk_agent] = fake_helpdesk_agent

    client: TestClient = TestClient(app)

    try:
        response: httpx2.Response = cast(
            httpx2.Response,
            client.post(  # type: ignore
                "/chat",
                json={
                    "message": "My laptop is not working.",
                },
            ),
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "response": "Test response: My laptop is not working.",
    }


def test_chat_endpoint_with_history() -> None:
    """Verify conversation history reaches the agent."""

    captured: dict[str, object] = {}

    class HistoryAgent:
        """Test agent that captures the request."""

        def process_request(
            self,
            request: ChatRequest,
        ) -> str:
            captured["request"] = request

            return "Context-aware response"

    def fake_current_user() -> dict[str, str]:
        """Return a test employee identity."""

        return {
            "username": "employee",
            "role": "employee",
        }

    def fake_agent() -> HistoryAgent:
        """Return the history test agent."""

        return HistoryAgent()

    app.dependency_overrides[get_current_user] = fake_current_user
    app.dependency_overrides[get_helpdesk_agent] = fake_agent

    client = TestClient(app)

    try:
        response = client.post(
            "/chat",
            json={
                "message": "What should I do next?",
                "history": [
                    {
                        "role": "user",
                        "content": "My VPN is not working.",
                    },
                    {
                        "role": "assistant",
                        "content": "Let's check your network connection.",
                    },
                ],
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "response": "Context-aware response",
    }

    request = captured["request"]

    assert isinstance(request, ChatRequest)
    assert len(request.history) == 2
    assert request.message == "What should I do next?"


def test_helpdesk_agent_includes_history() -> None:
    """Verify the agent sends history and the current message."""

    class FakeAIService:
        """Fake AI service."""

        def __init__(self) -> None:
            self.messages: list[ChatMessage] = []

        def generate_response(
            self,
            messages: list[ChatMessage],
        ) -> str:
            self.messages = messages
            return "Test response"

    ai_service = FakeAIService()
    agent = HelpdeskAgent(ai_service)

    request = ChatRequest(
        message="What should I do next?",
        history=[
            ChatMessage(
                role="user",
                content="VPN is not working.",
            ),
            ChatMessage(
                role="assistant",
                content="Let's check your connection.",
            ),
        ],
    )

    result = agent.process_request(request)

    assert result == "Test response"
    assert len(ai_service.messages) == 3

    assert ai_service.messages[-1] == ChatMessage(
        role="user",
        content="What should I do next?",
    )
