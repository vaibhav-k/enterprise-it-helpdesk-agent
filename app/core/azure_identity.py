"""
Azure identity provider.

Uses DefaultAzureCredential which automatically selects
the correct authentication method:

Local:
    Azure CLI credential

Azure hosting:
    Managed Identity

No secrets are stored in the application.
"""

from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential(exclude_interactive_browser_credential=True)


def get_azure_credential() -> DefaultAzureCredential:
    """
    Returns Azure credential provider.

    This credential works with:
    - Azure CLI locally
    - Managed Identity in Azure
    """

    return credential
