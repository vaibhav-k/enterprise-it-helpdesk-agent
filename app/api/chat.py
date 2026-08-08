"""
Helpdesk chat API.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.agents.helpdesk_agent import HelpdeskAgent
from app.core.security import get_current_user
from app.models.chat import ChatRequest, ChatResponse
from app.services.ai_service import AIService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


def get_helpdesk_agent() -> HelpdeskAgent:
    """
    Create the helpdesk agent.

    Returns:
        Configured helpdesk agent.
    """

    return HelpdeskAgent(AIService())


@router.post(
    "",
    status_code=status.HTTP_200_OK,
)
def chat(
    request: ChatRequest,
    user: Annotated[
        dict[str, str],
        Depends(get_current_user),
    ],
    agent: Annotated[
        HelpdeskAgent,
        Depends(get_helpdesk_agent),
    ],
) -> ChatResponse:
    """
    Process an authenticated helpdesk question.

    Args:
        request: Employee chat request.
        user: Authenticated application user.
        agent: Helpdesk agent.

    Returns:
        Generated helpdesk response.

    Raises:
        HTTPException: If AI processing fails.
    """

    del user

    try:
        response = agent.process_request(request)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI service could not process the request.",
        ) from exc

    return ChatResponse(response=response)
