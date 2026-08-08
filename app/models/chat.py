"""
Chat request and response models.
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request submitted to the helpdesk chat endpoint."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Employee helpdesk question.",
    )


class ChatResponse(BaseModel):
    """Response returned by the helpdesk chat endpoint."""

    response: str
