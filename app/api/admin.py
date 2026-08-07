"""
Admin-only API endpoints.
"""

from fastapi import (
    APIRouter,
    Depends,
)

from app.core.permissions import (
    Permission,
)
from app.core.security import (
    require_permission,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/users")
def list_users(
    user: dict[str, str] = Depends(require_permission(Permission.MANAGE_USERS)),
) -> dict[str, str]:
    """
    Admin-only user management endpoint.
    """

    return {
        "message": "Admin access granted",
        "user": user["username"],
    }
