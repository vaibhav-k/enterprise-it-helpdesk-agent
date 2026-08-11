"""
Chat request and response models.
"""

from typing import Literal

from pydantic import BaseModel, Field

ChatRole = Literal[
    "system",
    "user",
    "assistant",
]


class ChatMessage(BaseModel):
    """A message in the helpdesk conversation."""

    role: ChatRole

    content: str = Field(
        ...,
        min_length=1,
        max_length=20_000,
    )


class ChatRequest(BaseModel):
    """Request submitted to the helpdesk chat endpoint."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=4_000,
    )

    history: list[ChatMessage] = Field(
        default_factory=lambda: list[ChatMessage](),
        max_length=20,
    )

    session_id: str | None = Field(
        default=None,
        description=(
            "Existing chat session to continue. Omit to start a new "
            "session; the response will include the new session_id. "
            "When set, server-side session history is used instead "
            "of the `history` field."
        ),
    )


class ChatResponse(BaseModel):
    """Response returned by the helpdesk chat endpoint."""

    response: str

    session_id: str = Field(
        description="Session identifier. Pass this back on the next "
        "request in the same conversation to continue it.",
    )


class SessionSummary(BaseModel):
    """Summary of a stored chat session, without full message content."""

    session_id: str

    message_count: int

    created_at: float

    updated_at: float


class SessionDetail(BaseModel):
    """Full stored chat session, including message history."""

    session_id: str

    messages: list[ChatMessage]

    created_at: float

    updated_at: float
