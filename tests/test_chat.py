"""
Tests for the helpdesk chat API.
"""

from typing import cast

import httpx2
from fastapi.testclient import TestClient

from app.api.chat import get_helpdesk_agent
from app.core.security import get_current_user
from app.main import app


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
