"""
Temporary user repository.

This module provides an in-memory user store
for development.

Future replacement:

- Azure SQL
- PostgreSQL
- Cosmos DB
- Enterprise Identity Provider
"""

from app.core.security import hash_password
from app.models.user import User

users: list[User] = []


def seed_users() -> None:
    """
    Create default development users.

    Idempotent: calling this more than once (for example, once from
    the application startup and once from a test) will not create
    duplicate entries.
    """

    if get_user_by_username("employee"):
        return

    users.append(
        User(
            username="employee",
            password_hash=hash_password("Password123!"),
            role="employee",
        )
    )

    users.append(
        User(
            username="admin",
            password_hash=hash_password("Admin123!"),
            role="admin",
        )
    )


def get_user_by_username(
    username: str,
) -> User | None:
    """
    Find user by username.
    """

    for user in users:

        if user.username == username:

            return user

    return None


def create_user(
    username: str,
    password: str,
    role: str,
) -> User:
    """
    Create a new application user.

    Args:
        username:
            User login name.

        password:
            Plain text password.

        role:
            Application role.

    Returns:
        Created User object.
    """

    user = User(
        username=username,
        password_hash=hash_password(password),
        role=role,
    )

    users.append(user)

    return user
