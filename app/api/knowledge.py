"""
Knowledge base API endpoints.
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app.core.security import (
    get_current_user,
)
from app.services.storage_service import (
    list_documents,
)

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Base"],
)


@router.get("/documents")
def documents(
    user: dict[str, str] = Depends(get_current_user),
) -> dict[str, list[str]]:
    """
    Return knowledge base documents.

    Requires authentication.
    """

    try:
        files = list_documents()

        return {"documents": files}

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to access knowledge base",
        ) from exc
