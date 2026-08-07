from azure.core.credentials import TokenCredential

from app.core.azure_identity import get_azure_credential

credential: TokenCredential = get_azure_credential()


assert type(credential).__name__ == "DefaultAzureCredential"
