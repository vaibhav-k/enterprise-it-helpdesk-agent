from datetime import datetime, timedelta, timezone

from jose import jwt

from fastapi import Depends, HTTPException

from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from passlib.context import CryptContext


from app.core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


security_scheme = HTTPBearer()


def verify_password(password: str, hashed: str) -> bool:

    return password_context.verify(password, hashed)


def create_token(username: str, role: str) -> str:

    expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiry_minutes)

    payload = {"sub": username, "role": role, "exp": expiry}

    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> dict[str, str]:

    try:

        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )

        return {"username": str(payload["sub"]), "role": str(payload["role"])}

    except Exception as exc:

        raise HTTPException(status_code=401, detail="Invalid token") from exc
