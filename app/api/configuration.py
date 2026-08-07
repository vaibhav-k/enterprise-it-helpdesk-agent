"""
Secure configuration endpoints.
"""

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.services.keyvault_service import get_secret

router = APIRouter(
    prefix="/configuration",
    tags=["Configuration"],
)


@router.get("/secret/{name}")
def read_secret(
    name: str,
    user: dict[str, str] = Depends(get_current_user),
) -> dict[str, str]:
    """
    Retrieve Key Vault secret.

    Protected endpoint.
    """

    value = get_secret(name)

    return {"secret": value}
