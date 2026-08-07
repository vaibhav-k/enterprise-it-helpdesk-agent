"""
Authentication API endpoints.
"""

from fastapi import APIRouter, HTTPException

from app.core.security import (
    create_token,
)
from app.database.users import (
    get_user,
    verify_password,
)
from app.models.auth import (
    LoginRequest,
    TokenResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
) -> TokenResponse:
    """
    Authenticate user and return JWT token.
    """

    user = get_user(request.username)

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    password_valid = verify_password(
        request.password,
        user.password_hash,
    )

    if not password_valid:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    token = create_token(
        username=user.username,
        role=user.role,
    )

    return TokenResponse(
        access_token=token,
    )
