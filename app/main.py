"""
Enterprise IT Helpdesk Agent API.
"""

from fastapi import FastAPI

from app.api import (
    admin,
    auth,
    chat,
    configuration,
    knowledge,
    tickets,
)
from app.core.logging import (
    configure_logging,
)
from app.middleware.audit import (
    AuditMiddleware,
)

configure_logging()

app = FastAPI(
    title="Enterprise IT Helpdesk Agent",
)

app.include_router(admin.router)

app.add_middleware(AuditMiddleware)

app.include_router(auth.router)

app.include_router(chat.router)

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
