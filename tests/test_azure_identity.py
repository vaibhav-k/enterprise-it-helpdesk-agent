"""
Azure identity tests.
"""

from azure.identity import DefaultAzureCredential

from app.core.azure_identity import (
    get_azure_credential,
)


def test_azure_credential_type() -> None:
    """
    Verify Azure credential factory.
    """

    credential = get_azure_credential()

    assert isinstance(
        credential,
        DefaultAzureCredential,
    )
