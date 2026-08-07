"""
Ticket data models.

Defines helpdesk ticket request and response structures.
"""

from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    """
    Request model for creating tickets.
    """

    title: str = Field(
        min_length=5,
        max_length=100,
        description="Ticket title",
    )

    description: str = Field(
        min_length=10,
        max_length=500,
        description="Ticket description",
    )


class TicketResponse(BaseModel):
    """
    Ticket response model.
    """

    id: int

    title: str

    description: str

    created_by: str

    status: str
