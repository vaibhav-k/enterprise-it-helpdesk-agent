from dataclasses import dataclass

from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class User:

    username: str

    password_hash: str

    role: str


_users = {
    "employee@test.com": User(
        username="employee@test.com",
        password_hash=password_context.hash("Password123!"),
        role="employee",
    ),
    "admin@test.com": User(
        username="admin@test.com",
        password_hash=password_context.hash("Admin123!"),
        role="admin",
    ),
}


def get_user(username: str) -> User | None:

    return _users.get(username)
