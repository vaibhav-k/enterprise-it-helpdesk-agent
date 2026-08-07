"""
JWT token generation tests.
"""

from app.core.security import (
    create_access_token,
)


def test_create_access_token() -> None:
    """
    Verify JWT token generation.
    """

    token = create_access_token(
        {
            "email": "employee@test.com",
            "role": "employee",
        }
    )

    assert token is not None
    assert isinstance(token, str)
