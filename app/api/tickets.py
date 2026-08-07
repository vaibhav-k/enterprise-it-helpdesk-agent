from fastapi import APIRouter, Depends

from app.core.security import current_user
from app.models.ticket import TicketCreate, TicketResponse

router = APIRouter(prefix="/tickets", tags=["tickets"])


tickets: list[TicketResponse] = []


@router.post("", response_model=TicketResponse)
def create_ticket(
    ticket: TicketCreate, user: dict[str, str] = Depends(current_user)
) -> TicketResponse:

    item = TicketResponse(
        id=len(tickets) + 1,
        title=ticket.title,
        description=ticket.description,
        created_by=user["username"],
    )

    tickets.append(item)

    return item
