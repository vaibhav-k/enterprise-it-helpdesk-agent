"""
Chat request and response models.

These models define the request and response payloads
used by the Helpdesk Agent chat API.
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Chat request sent by a client.
    """

    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Employee question.",
    )


class ChatResponse(BaseModel):
    """
    Chat response returned by the Helpdesk Agent.
    """

    response: str = Field(
        ...,
        description="Agent response.",
    )
