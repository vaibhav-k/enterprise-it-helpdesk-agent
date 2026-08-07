"""
Application security utilities.

Provides:

- Password verification
- JWT token creation
- JWT token validation
"""

from collections.abc import Callable

from fastapi import Depends, HTTPException

from app.core.permissions import (
    ROLE_PERMISSIONS,
    Permission,
    Role,
)
from app.core.security import get_current_user


def require_permission(
    permission: Permission,
):
    """
    Create permission dependency.
    """

    def checker(
        user: dict[str, str] = Depends(get_current_user),
    ) -> dict[str, str]:

        if not has_permission(
            user["role"],
            permission,
        ):

            raise HTTPException(
                status_code=403,
                detail=("Permission denied"),
            )

        return user

    return checker


def require_role(
    required_role: str,
) -> Callable:
    """
    Validate user role.
    """

    def role_checker(
        user: dict[str, str] = Depends(get_current_user),
    ) -> dict[str, str]:

        if user["role"] != required_role:

            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions",
            )

        return user

    return role_checker


def has_permission(
    role: str,
    permission: Permission,
) -> bool:
    """
    Check whether role has permission.

    Args:
        role:
            User role.

        permission:
            Required permission.

    Returns:
        True if allowed.
    """

    try:

        user_role = Role(role)

    except ValueError:

        return False

    return permission in ROLE_PERMISSIONS[user_role]
