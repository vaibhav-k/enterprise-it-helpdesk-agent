"""
Secure configuration endpoints.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.services.keyvault_service import get_secret

router = APIRouter(
    prefix="/configuration",
    tags=["Configuration"],
)


CurrentUser = Annotated[
    dict[str, str],
    Depends(get_current_user),
]


@router.get(
    "/secret/{name}",
)
def read_secret(
    name: str,
    user: CurrentUser,
) -> dict[str, str]:
    """
    Retrieve a secret from Azure Key Vault.

    The endpoint requires an authenticated user.
    Missing secrets return HTTP 404 instead of returning ``None``.
    """

    # Keep the dependency explicit so authentication is enforced.
    _ = user

    value = get_secret(name)

    if value is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Secret not found.",
        )

    return {
        "secret": value,
    }
