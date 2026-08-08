"""
Chat API endpoints.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.agents.helpdesk_agent import HelpdeskAgent
from app.core.security import get_current_user
from app.models.chat import ChatRequest, ChatResponse
from app.services.ai_service import AIService
from app.services.knowledge_service import KnowledgeService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
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


@router.post("")
def chat(
    request: ChatRequest,
    _: Annotated[
        dict[str, str],
        Depends(get_current_user),
    ],
    agent: Annotated[
        HelpdeskAgent,
        Depends(get_helpdesk_agent),
    ],
) -> ChatResponse:
    """
    Process an authenticated helpdesk chat request.

    Args:
        request: Employee chat request.
        _: Authenticated employee identity.
        agent: Helpdesk agent dependency.

    Returns:
        Generated helpdesk response.
    """

    response = agent.process_request(request)

    return ChatResponse(
        response=response,
    )
