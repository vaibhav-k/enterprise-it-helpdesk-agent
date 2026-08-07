"""
User repository tests.
"""

from app.database.users import (
    get_user_by_username,
    seed_users,
)


def test_get_existing_user() -> None:
    seed_users()

    user = get_user_by_username(
        "employee",
    )

    assert user is not None
