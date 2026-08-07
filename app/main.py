from fastapi import FastAPI

from app.api import auth, tickets, health

app = FastAPI(title="Enterprise IT Helpdesk Agent")


app.include_router(auth.router)

app.include_router(tickets.router)

app.include_router(health.router)
