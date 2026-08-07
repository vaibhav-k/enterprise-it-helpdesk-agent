"""
User data models.

Defines application user structures.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """
    Represents an application user.
    """

    username: str

    password_hash: str

    role: str
