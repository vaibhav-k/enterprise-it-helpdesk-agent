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


class ChatResponse(BaseModel):
    """Response returned by the helpdesk chat endpoint."""

    response: str
