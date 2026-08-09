"""
Authentication request and response models.
"""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """
    User login request.
    """

    username: str = Field(
        min_length=3,
        description="User login name",
    )

    password: str = Field(
        min_length=8,
        max_length=72,
        description="User password",
    )


class TokenResponse(BaseModel):
    """
    JWT token response.
    """

    access_token: str

    token_type: str = "bearer"
