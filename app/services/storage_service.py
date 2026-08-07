"""
Azure Blob Storage service.

Provides secure access to the Helpdesk knowledge base.

Authentication:

Local:
    Azure CLI Credential

Azure Hosting:
    Managed Identity

Provided through:

DefaultAzureCredential
"""

from azure.storage.blob import (
    BlobServiceClient,
)

from app.core.azure_identity import (
    get_azure_credential,
)
from app.core.config import (
    settings,
)


def get_storage_client() -> BlobServiceClient:
    """
    Create Azure Blob Storage client.

    Returns:
        BlobServiceClient instance.
    """

    account_url = (
        f"https://" f"{settings.azure_storage_account}" f".blob.core.windows.net"
    )

    return BlobServiceClient(
        account_url=account_url,
        credential=get_azure_credential(),
    )


def list_documents() -> list[str]:
    """
    List knowledge base documents.

    Returns:
        List of blob names.
    """

    client = get_storage_client()

    container = client.get_container_client(settings.azure_container)

    return [blob.name for blob in container.list_blobs()]
