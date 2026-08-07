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

from passlib.context import CryptContext

from app.models.user import User

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Create secure password hash.

    Args:
        password:
            Plain text password.

    Returns:
        BCrypt password hash.
    """

    return password_context.hash(password)


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    """
    Verify user password.

    Args:
        password:
            Plain text password.

        password_hash:
            Stored password hash.

    Returns:
        True if password matches.
    """

    return password_context.verify(
        password,
        password_hash,
    )


_users: dict[str, User] = {
    "employee@test.com": User(
        username="employee@test.com",
        password_hash=hash_password("Password123!"),
        role="employee",
    ),
    "admin@test.com": User(
        username="admin@test.com",
        password_hash=hash_password("Admin123!"),
        role="admin",
    ),
}


def get_user(
    username: str,
) -> User | None:
    """
    Retrieve user by username.

    Args:
        username:
            User login identifier.

    Returns:
        User object or None.
    """

    return _users.get(username)


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

    _users[username] = user

    return user
