"""
Azure Key Vault service.

Provides secure secret retrieval using
DefaultAzureCredential.

Authentication:

Local Development:
    Azure CLI credential

Azure Deployment:
    Managed Identity
"""

from azure.keyvault.secrets import (
    SecretClient,
)

from app.core.azure_identity import (
    get_azure_credential,
)
from app.core.config import (
    settings,
)


def get_keyvault_client() -> SecretClient:
    """
    Create Azure Key Vault client.

    Returns:
        SecretClient instance.
    """

    vault_url = f"https://" f"{settings.keyvault_name}" f".vault.azure.net"

    return SecretClient(
        vault_url=vault_url,
        credential=get_azure_credential(),
    )


def get_secret(
    secret_name: str,
) -> str | None:
    """
    Retrieve secret from Azure Key Vault.

    Args:
        secret_name:
            Name of secret.

    Returns:
        Secret value.
    """

    client = get_keyvault_client()

    secret = client.get_secret(secret_name)

    return secret.value
