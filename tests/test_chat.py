"""
Tests for the helpdesk agent.
"""

from app.agents.helpdesk_agent import HelpdeskAgent
from app.models.chat import ChatMessage, ChatRequest
from app.models.knowledge import (
    KnowledgeContext,
    KnowledgeDocument,
)


class FakeAIService:
    """Fake AI service for deterministic tests."""

    def __init__(self) -> None:
        """Initialize captured messages."""

        self.messages: list[ChatMessage] = []

    def generate_response(
        self,
        messages: list[ChatMessage],
    ) -> str:
        """Capture messages and return a test response."""

        self.messages = messages

        return "Test response"


class FakeKnowledgeService:
    """Fake knowledge service for deterministic tests."""

    def __init__(
        self,
        context: KnowledgeContext,
    ) -> None:
        """Initialize with a fixed knowledge context."""

        self._context = context
        self.query: str | None = None

    def get_context(
        self,
        query: str,
        *,
        max_documents: int = 5,
    ) -> KnowledgeContext:
        """Capture the query and return test knowledge."""

        self.query = query

        assert max_documents == 5

        return self._context


def test_helpdesk_agent_adds_knowledge_context() -> None:
    """Verify retrieved knowledge reaches the AI service."""

    ai_service = FakeAIService()

    knowledge_service = FakeKnowledgeService(
        KnowledgeContext(
            documents=[
                KnowledgeDocument(
                    name="vpn-guide.txt",
                    content=(
                        "Restart the VPN client and verify " "network connectivity."
                    ),
                ),
            ],
        ),
    )

    agent = HelpdeskAgent(
        ai_service=ai_service,
        knowledge_service=knowledge_service,
    )

    request = ChatRequest(
        message="My VPN is not working.",
    )

    result = agent.process_request(request)

    assert result == "Test response"

    assert knowledge_service.query == ("My VPN is not working.")

    assert len(ai_service.messages) == 2

    assert ai_service.messages[0].role == "system"
    assert "vpn-guide.txt" in ai_service.messages[0].content
    assert "Restart the VPN client" in (ai_service.messages[0].content)

    assert ai_service.messages[1] == ChatMessage(
        role="user",
        content="My VPN is not working.",
    )


def test_helpdesk_agent_preserves_history() -> None:
    """Verify knowledge and conversation history are preserved."""

    ai_service = FakeAIService()

    knowledge_service = FakeKnowledgeService(
        KnowledgeContext(),
    )

    agent = HelpdeskAgent(
        ai_service=ai_service,
        knowledge_service=knowledge_service,
    )

    request = ChatRequest(
        message="What should I do next?",
        history=[
            ChatMessage(
                role="user",
                content="My VPN is not working.",
            ),
            ChatMessage(
                role="assistant",
                content="Let's check your connection.",
            ),
        ],
    )

    agent.process_request(request)

    assert len(ai_service.messages) == 3

    assert ai_service.messages[0].role == "user"
    assert ai_service.messages[1].role == "assistant"
    assert ai_service.messages[2].role == "user"


def test_helpdesk_agent_without_knowledge() -> None:
    """Verify the agent works when retrieval finds nothing."""

    ai_service = FakeAIService()

    knowledge_service = FakeKnowledgeService(
        KnowledgeContext(),
    )

    agent = HelpdeskAgent(
        ai_service=ai_service,
        knowledge_service=knowledge_service,
    )

    result = agent.process_request(
        ChatRequest(
            message="Hello",
        ),
    )

    assert result == "Test response"

    assert len(ai_service.messages) == 1

    assert ai_service.messages[0] == ChatMessage(
        role="user",
        content="Hello",
    )
