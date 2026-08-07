"""
Application security utilities.

Provides:

- Password verification
- JWT token creation
- JWT token validation
"""

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jose import JWTError, jwt

from app.core.config import settings

security_scheme = HTTPBearer()


def create_token(
    username: str,
    role: str,
) -> str:
    """
    Create JWT access token.

    Args:
        username:
            User identifier.

        role:
            Application role.

    Returns:
        Encoded JWT token.
    """

    expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiry_minutes)

    payload = {
        "sub": username,
        "role": role,
        "exp": expiry,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> dict[str, str]:
    """
    Validate JWT token.

    Returns:
        Authenticated user information.

    Raises:
        HTTPException:
            When token is invalid.
    """

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )

    except JWTError as exc:

        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
        ) from exc

    username = payload.get("sub")

    role = payload.get("role")

    if not isinstance(username, str) or not isinstance(role, str):

        raise HTTPException(
            status_code=401,
            detail="Invalid token payload",
        )

    return {
        "username": username,
        "role": role,
    }
