"""
Enterprise IT Helpdesk Agent API.
"""

from fastapi import FastAPI

from app.api import (
    admin,
    auth,
    configuration,
    knowledge,
    tickets,
)

app = FastAPI(
    title="Enterprise IT Helpdesk Agent",
)

app.include_router(admin.router)

app.include_router(auth.router)

app.include_router(configuration.router)

app.include_router(knowledge.router)

app.include_router(tickets.router)


@app.get("/")
def root() -> dict[str, str]:
    """
    Application root endpoint.
    """

    return {
        "application": "Enterprise IT Helpdesk Agent",
        "status": "running",
    }
