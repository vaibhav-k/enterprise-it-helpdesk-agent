"""
Tests for the helpdesk chat API: sessions, rate limiting, and identity
propagation.
"""

from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient

from app.api.chat import chat_rate_limiter, get_helpdesk_agent
from app.core.security import get_current_user
from app.database import sessions
from app.main import app
from app.models.chat import ChatRequest


class FakeHelpdeskAgent:
    """Fake helpdesk agent for API tests."""

    def __init__(self) -> None:
        """Initialize captured call arguments."""

        self.requesting_user: str | None = None

    def process_request(
        self,
        request: ChatRequest,
        *,
        requesting_user: str | None = None,
    ) -> str:
        """
        Return a deterministic response.

        Args:
            request: Helpdesk chat request.
            requesting_user: Authenticated username, if provided.

        Returns:
            Fake helpdesk response.
        """

        self.requesting_user = requesting_user

        return f"Test response: {request.message}"


def _fake_current_user(username: str = "employee") -> Callable[[], dict[str, str]]:
    """Build a fake authenticated-user dependency override."""

    def dependency() -> dict[str, str]:
        return {"username": username, "role": "employee"}

    return dependency


@pytest.fixture(autouse=True)
def _clean_state():
    """Reset shared in-memory state between tests."""

    sessions.clear_all()
    chat_rate_limiter.reset()

    yield

    sessions.clear_all()
    chat_rate_limiter.reset()
    app.dependency_overrides.clear()


def test_chat_endpoint_creates_a_new_session() -> None:
    """Verify a chat request with no session_id starts a new session."""

    fake_agent = FakeHelpdeskAgent()

    app.dependency_overrides[get_current_user] = _fake_current_user()
    app.dependency_overrides[get_helpdesk_agent] = lambda: fake_agent

    client = TestClient(app)

    response = client.post(
        "/chat",
        json={"message": "My laptop is not working."},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["response"] == "Test response: My laptop is not working."
    assert body["session_id"]

    # The response was persisted server-side.
    stored = sessions.get_session(body["session_id"], owner="employee")

    assert stored is not None
    assert len(stored.messages) == 2
    assert stored.messages[0].content == "My laptop is not working."
    assert stored.messages[1].content == body["response"]


def test_chat_endpoint_continues_an_existing_session() -> None:
    """Verify passing session_id continues the same conversation."""

    fake_agent = FakeHelpdeskAgent()

    app.dependency_overrides[get_current_user] = _fake_current_user()
    app.dependency_overrides[get_helpdesk_agent] = lambda: fake_agent

    client = TestClient(app)

    first = client.post("/chat", json={"message": "My VPN is down."})
    session_id = first.json()["session_id"]

    second = client.post(
        "/chat",
        json={"message": "What next?", "session_id": session_id},
    )

    assert second.status_code == 200
    assert second.json()["session_id"] == session_id

    stored = sessions.get_session(session_id, owner="employee")

    assert stored is not None
    assert len(stored.messages) == 4
    assert [m.content for m in stored.messages] == [
        "My VPN is down.",
        "Test response: My VPN is down.",
        "What next?",
        "Test response: What next?",
    ]


def test_chat_endpoint_rejects_another_users_session_id() -> None:
    """Verify a session_id owned by a different user is treated as 404."""

    other_session = sessions.create_session(owner="someone-else")

    fake_agent = FakeHelpdeskAgent()

    app.dependency_overrides[get_current_user] = _fake_current_user("employee")
    app.dependency_overrides[get_helpdesk_agent] = lambda: fake_agent

    client = TestClient(app)

    response = client.post(
        "/chat",
        json={
            "message": "Hello",
            "session_id": other_session.session_id,
        },
    )

    assert response.status_code == 404


def test_chat_endpoint_propagates_authenticated_identity() -> None:
    """Verify the authenticated username reaches the helpdesk agent."""

    fake_agent = FakeHelpdeskAgent()

    app.dependency_overrides[get_current_user] = _fake_current_user("employee")
    app.dependency_overrides[get_helpdesk_agent] = lambda: fake_agent

    client = TestClient(app)

    client.post("/chat", json={"message": "Hello"})

    assert fake_agent.requesting_user == "employee"


def test_chat_endpoint_enforces_rate_limit() -> None:
    """Verify repeated requests beyond the limit return 429."""

    fake_agent = FakeHelpdeskAgent()

    app.dependency_overrides[get_current_user] = _fake_current_user()
    app.dependency_overrides[get_helpdesk_agent] = lambda: fake_agent

    client = TestClient(app)

    max_requests = chat_rate_limiter.max_requests

    for _ in range(max_requests):
        response = client.post("/chat", json={"message": "Hello"})
        assert response.status_code == 200

    limited = client.post("/chat", json={"message": "Hello"})

    assert limited.status_code == 429
    assert "Retry-After" in limited.headers


def test_sessions_are_scoped_per_user() -> None:
    """Verify one user cannot list or read another user's sessions."""

    fake_agent = FakeHelpdeskAgent()

    app.dependency_overrides[get_current_user] = _fake_current_user("employee")
    app.dependency_overrides[get_helpdesk_agent] = lambda: fake_agent

    client = TestClient(app)

    created = client.post("/chat", json={"message": "Hello"})
    session_id = created.json()["session_id"]

    app.dependency_overrides[get_current_user] = _fake_current_user("someone-else")

    listing = client.get("/chat/sessions")
    assert listing.json() == []

    detail = client.get(f"/chat/sessions/{session_id}")
    assert detail.status_code == 404

    deletion = client.delete(f"/chat/sessions/{session_id}")
    assert deletion.status_code == 404


def test_list_and_delete_own_sessions() -> None:
    """Verify a user can list and delete their own sessions."""

    fake_agent = FakeHelpdeskAgent()

    app.dependency_overrides[get_current_user] = _fake_current_user("employee")
    app.dependency_overrides[get_helpdesk_agent] = lambda: fake_agent

    client = TestClient(app)

    created = client.post("/chat", json={"message": "Hello"})
    session_id = created.json()["session_id"]

    listing = client.get("/chat/sessions")
    assert listing.status_code == 200
    assert [s["session_id"] for s in listing.json()] == [session_id]

    detail = client.get(f"/chat/sessions/{session_id}")
    assert detail.status_code == 200
    assert len(detail.json()["messages"]) == 2

    deletion = client.delete(f"/chat/sessions/{session_id}")
    assert deletion.status_code == 204

    listing_after = client.get("/chat/sessions")
    assert listing_after.json() == []
