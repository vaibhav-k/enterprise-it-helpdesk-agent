from fastapi import APIRouter, HTTPException

from app.database.users import get_user

from app.models.auth import LoginRequest, TokenResponse

from app.core.security import verify_password, create_token

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest) -> TokenResponse:

    user = get_user(request.username)

    if user is None:

        raise HTTPException(401, "Invalid credentials")

    if not verify_password(request.password, user.password_hash):

        raise HTTPException(401, "Invalid credentials")

    return TokenResponse(access_token=create_token(user.username, user.role))
