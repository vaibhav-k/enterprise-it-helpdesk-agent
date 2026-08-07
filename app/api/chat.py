"""
Chat API endpoints.

Provides authenticated access to the
Enterprise IT Helpdesk Agent.
"""

from fastapi import (
    APIRouter,
    Depends,
)

from app.agents.helpdesk_agent import (
    HelpdeskAgent,
)
from app.core.logging import (
    get_logger,
)
from app.core.security import (
    get_current_user,
)
from app.models.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.ai_service import (
    AIService,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


logger = get_logger(
    "chat_api",
)


def get_helpdesk_agent() -> HelpdeskAgent:
    """
    Create HelpdeskAgent instance.

    Returns:
        Configured helpdesk agent.
    """

    return HelpdeskAgent(
        ai_service=AIService(),
    )


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    user: dict[str, str] = Depends(
        get_current_user,
    ),
    agent: HelpdeskAgent = Depends(
        get_helpdesk_agent,
    ),
) -> ChatResponse:
    """
    Process employee helpdesk request.

    Args:
        request:
            Employee question.

        user:
            Authenticated user.

        agent:
            Helpdesk agent instance.

    Returns:
        AI generated response.
    """

    logger.info(
        "chat_request username=%s",
        user["username"],
    )

    response = agent.process_request(
        request.message,
    )

    return ChatResponse(
        response=response,
    )
