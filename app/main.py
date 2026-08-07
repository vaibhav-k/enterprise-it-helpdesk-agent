"""
To use this application, run the following command:

    uvicorn app.main:app --reload

Then, open your browser and navigate to http://localhost:8000/docs to access the
interactive API documentation.

Test:

POST /auth/login

Request:

    {
    "username": "employee@test.com",
    "password": "Password123!"
    }

Response:

    {
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer"
    }
"""

from fastapi import FastAPI

from app.api import auth

app = FastAPI(
    title="Enterprise IT Helpdesk Agent",
)


app.include_router(
    auth.router,
)


@app.get("/")
def root() -> dict[str, str]:

    return {
        "application": "Enterprise IT Helpdesk Agent",
        "status": "running",
    }
