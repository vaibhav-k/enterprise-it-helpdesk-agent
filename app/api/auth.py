"""
Authentication API endpoints.

Provides:

- User login
- JWT token generation
- Authentication audit logging
"""

from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from app.core.logging import (
    get_logger,
)
from app.core.security import (
    create_access_token,
    verify_password,
)
from app.database.users import (
    get_user_by_username,
)
from app.models.auth import (
    LoginRequest,
    TokenResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


logger = get_logger(
    "authentication",
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
) -> TokenResponse:
    """
    Authenticate user and issue JWT token.

    Args:
        request:
            User login credentials.

    Returns:
        JWT access token.

    Raises:
        HTTPException:
            When authentication fails.
    """

    user = get_user_by_username(request.username)

    if user is None:

        logger.warning(
            "failed_login username=%s reason=user_not_found",
            request.username,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    password_valid = verify_password(
        request.password,
        user.password_hash,
    )

    if not password_valid:

        logger.warning(
            "failed_login username=%s reason=invalid_password",
            request.username,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token_payload = {
        "sub": user.username,
        "role": user.role,
    }

    access_token = create_access_token(
        data=token_payload,
    )

    logger.info(
        "successful_login username=%s role=%s",
        user.username,
        user.role,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )
