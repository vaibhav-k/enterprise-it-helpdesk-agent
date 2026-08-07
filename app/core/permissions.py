"""
Application authorization model.

Defines roles and permissions.

This is application-level RBAC.

Azure RBAC will control
Azure resource access separately.
"""

from enum import Enum


class Role(str, Enum):
    """
    Application user roles.
    """

    EMPLOYEE = "employee"

    ADMIN = "admin"


class Permission(str, Enum):
    """
    Application permissions.
    """

    CREATE_TICKET = "ticket:create"

    VIEW_TICKETS = "ticket:view"

    MANAGE_USERS = "user:manage"


ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.EMPLOYEE: {
        Permission.CREATE_TICKET,
        Permission.VIEW_TICKETS,
    },
    Role.ADMIN: {
        Permission.CREATE_TICKET,
        Permission.VIEW_TICKETS,
        Permission.MANAGE_USERS,
    },
}
