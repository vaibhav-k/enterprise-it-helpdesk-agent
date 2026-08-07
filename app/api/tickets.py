"""
Helpdesk ticket API endpoints.
"""

from fastapi import APIRouter, Depends

from app.core.permissions import (
    Permission,
)
from app.core.security import (
    get_current_user,
    require_permission,
)
from app.models.ticket import (
    TicketCreate,
    TicketResponse,
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


tickets: list[TicketResponse] = []


@router.post(
    "",
    response_model=TicketResponse,
)
def create_ticket(
    ticket: TicketCreate,
    user: dict[str, str] = Depends(require_permission(Permission.CREATE_TICKET)),
) -> TicketResponse:
    """
    Create a new helpdesk ticket.

    Requires authenticated user.
    """

    new_ticket = TicketResponse(
        id=len(tickets) + 1,
        title=ticket.title,
        description=ticket.description,
        created_by=user["username"],
        status="Open",
    )

    tickets.append(new_ticket)

    return new_ticket


@router.get(
    "",
    response_model=list[TicketResponse],
)
def list_tickets(
    user: dict[str, str] = Depends(get_current_user),
) -> list[TicketResponse]:
    """
    Return available tickets.

    Requires authentication.
    """

    return tickets
