from pydantic import BaseModel


class TicketCreate(BaseModel):

    title: str

    description: str


class TicketResponse(BaseModel):

    id: int

    title: str

    description: str

    created_by: str
