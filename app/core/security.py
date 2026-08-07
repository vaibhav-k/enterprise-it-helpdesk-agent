"""
Application security utilities.

Provides:

- Password verification
- JWT token creation
- JWT token validation
"""

from collections.abc import Callable

from fastapi import Depends, HTTPException

from app.core.security import get_current_user


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
