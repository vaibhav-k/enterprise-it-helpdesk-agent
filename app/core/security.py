"""
Security utilities.

Contains:

- Password hashing
- Password verification
- JWT token creation
- JWT validation
- Authorization helpers
"""

from collections.abc import Callable
from datetime import (
    datetime,
    timedelta,
    timezone,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jose import (
    JWTError,
    jwt,
)
from passlib.context import (
    CryptContext,
)

from app.core.config import (
    settings,
)
from app.core.permissions import (
    ROLE_PERMISSIONS,
    Permission,
    Role,
)

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


bearer_scheme = HTTPBearer()


def hash_password(
    password: str,
) -> str:
    """
    Hash plain password.
    """

    return password_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify password against hash.
    """

    return password_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    data: dict[str, str],
) -> str:
    """
    Create JWT access token.
    """

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiry_minutes)

    payload["exp"] = expire

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict[str, str]:
    """
    Validate JWT token.
    """

    try:

        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )

    except JWTError as exc:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc

    username = payload.get("sub")
    role = payload.get("role")

    if not username or not role:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    return {
        "username": username,
        "role": role,
    }


def has_permission(
    role: str,
    permission: Permission,
) -> bool:
    """
    Check role permissions.
    """

    try:

        user_role = Role(role)

    except ValueError:

        return False

    return permission in ROLE_PERMISSIONS[user_role]


def require_permission(
    permission: Permission,
) -> Callable:
    """
    FastAPI authorization dependency.
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
                detail="Permission denied",
            )

        return user

    return checker
