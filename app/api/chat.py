"""
Chat API endpoints.

Provides:

- Turn-based helpdesk chat, backed by server-side session persistence
- Per-user rate limiting
- Session listing, retrieval, and deletion
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.agents.helpdesk_agent import HelpdeskAgent
from app.core.config import settings
from app.core.rate_limit import (
    RateLimiter,
    make_user_rate_limit_dependency,
)
from app.core.security import get_current_user
from app.database import sessions
from app.models.chat import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    SessionDetail,
    SessionSummary,
)
from app.services.ai_service import AIService
from app.services.knowledge_service import KnowledgeService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

CurrentUser = Annotated[
    dict[str, str],
    Depends(get_current_user),
]

# Per-user: chat calls Azure OpenAI, which is the most expensive and
# most abuse-sensitive operation in the app, so it is limited by
# authenticated identity rather than by IP.
chat_rate_limiter = RateLimiter(
    max_requests=settings.rate_limit_chat_max_requests,
    window_seconds=settings.rate_limit_chat_window_seconds,
)

_chat_rate_limit_dependency = Depends(
    make_user_rate_limit_dependency(chat_rate_limiter),
)


def get_ai_service() -> AIService:
    """
    Provide the configured AI service.

    Returns:
        Azure OpenAI service instance.
    """

    return AIService()


def get_knowledge_service() -> KnowledgeService:
    """
    Provide the configured knowledge service.

    Returns:
        Azure Blob Storage knowledge service instance.
    """

    return KnowledgeService()


def get_helpdesk_agent(
    ai_service: Annotated[
        AIService,
        Depends(get_ai_service),
    ],
    knowledge_service: Annotated[
        KnowledgeService,
        Depends(get_knowledge_service),
    ],
) -> HelpdeskAgent:
    """
    Provide the helpdesk agent.

    Args:
        ai_service: Configured AI provider.
        knowledge_service: Configured knowledge provider.

    Returns:
        Application helpdesk agent.
    """

    return HelpdeskAgent(
        ai_service=ai_service,
        knowledge_service=knowledge_service,
    )


def _get_owned_session_or_404(
    session_id: str,
    owner: str,
) -> sessions.ChatSession:
    """
    Look up a session, or raise 404 if missing or not owned by ``owner``.

    Args:
        session_id: Session identifier from the request.
        owner: Authenticated username expected to own the session.

    Returns:
        The matching session.

    Raises:
        HTTPException: 404 if no such session exists for this owner.
            A session that exists but belongs to someone else returns
            the same 404 as a session that doesn't exist at all, so
            the endpoint never confirms another user's session ID.
    """

    session = sessions.get_session(session_id, owner=owner)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found.",
        )

    return session


@router.post(
    "",
    dependencies=[_chat_rate_limit_dependency],
)
def chat(
    request: ChatRequest,
    user: CurrentUser,
    agent: Annotated[
        HelpdeskAgent,
        Depends(get_helpdesk_agent),
    ],
) -> ChatResponse:
    """
    Process an authenticated helpdesk chat request.

    Continues an existing session when ``session_id`` is provided
    (server-side history is used and the client-supplied ``history``
    is ignored), or starts a new session otherwise. Rate-limited per
    authenticated user.

    Args:
        request: Employee chat request.
        user: Authenticated employee identity.
        agent: Helpdesk agent dependency.

    Returns:
        Generated helpdesk response, with the session ID to continue
        the conversation.

    Raises:
        HTTPException: 404 if ``session_id`` is provided but does not
            belong to the authenticated user.
    """

    if request.session_id is not None:
        session = _get_owned_session_or_404(
            request.session_id,
            owner=user["username"],
        )
    else:
        session = sessions.create_session(owner=user["username"])

    agent_request = ChatRequest(
        message=request.message,
        history=session.messages,
    )

    response_text = agent.process_request(
        agent_request,
        requesting_user=user["username"],
    )

    sessions.append_turn(
        session,
        user_message=ChatMessage(role="user", content=request.message),
        assistant_message=ChatMessage(role="assistant", content=response_text),
    )

    return ChatResponse(
        response=response_text,
        session_id=session.session_id,
    )


@router.get(
    "/sessions",
    response_model=list[SessionSummary],
)
def list_sessions(
    user: CurrentUser,
) -> list[SessionSummary]:
    """
    List the authenticated user's chat sessions.

    Only sessions owned by the caller are returned.
    """

    return [
        SessionSummary(
            session_id=session.session_id,
            message_count=len(session.messages),
            created_at=session.created_at,
            updated_at=session.updated_at,
        )
        for session in sessions.list_sessions(owner=user["username"])
    ]


@router.get(
    "/sessions/{session_id}",
    response_model=SessionDetail,
)
def get_session(
    session_id: str,
    user: CurrentUser,
) -> SessionDetail:
    """
    Retrieve a chat session's full message history.

    Requires the authenticated user to own the session.
    """

    session = _get_owned_session_or_404(session_id, owner=user["username"])

    return SessionDetail(
        session_id=session.session_id,
        messages=session.messages,
        created_at=session.created_at,
        updated_at=session.updated_at,
    )


@router.delete(
    "/sessions/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_session(
    session_id: str,
    user: CurrentUser,
) -> None:
    """
    Delete a chat session.

    Requires the authenticated user to own the session.
    """

    deleted = sessions.delete_session(session_id, owner=user["username"])

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found.",
        )
