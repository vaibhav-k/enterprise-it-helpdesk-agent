"""
Enterprise IT Helpdesk Agent API.

Run the application with:
uvicorn app.main:app --reload

Access the interactive Swagger UI at:
http://localhost:8000/docs

Authentication is required for all endpoints except the root and health
check endpoints.

To authenticate:

1. Open the Swagger UI in your browser:
   http://127.0.0.1:8000/docs

2. Call POST /auth/login with the following JSON payload:

   {
       "username": "employee",
       "password": "Password123!"
   }

3. Copy the access_token from the response.

4. Click Authorize at the top of the Swagger UI and paste the token.

5. You can now interact with authenticated endpoints such as:

   * /chat
   * /tickets
   * /knowledge/documents

The `POST /chat` endpoint is used to interact with the AI assistant.
It requires a JSON payload containing a `message` field with the user's
query.

Example request:

{
    "message": "How do I reset my password?",
    "history": [
        {
            "role": "user",
            "content": "How do I reset my password?"
        }
    ]
}

This request can be sent to POST /chat from the Swagger UI or through
any HTTP client.
"""

from fastapi import FastAPI

from app.api import (
    admin,
    auth,
    chat,
    configuration,
    health,
    knowledge,
    tickets,
)
from app.core.logging import configure_logging
from app.database.users import seed_users
from app.middleware.audit import AuditMiddleware

configure_logging()

seed_users()

app = FastAPI(
    title="Enterprise IT Helpdesk Agent",
)

app.include_router(admin.router)

app.add_middleware(AuditMiddleware)

app.include_router(auth.router)

app.include_router(chat.router)

app.include_router(configuration.router)

app.include_router(health.router)

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
