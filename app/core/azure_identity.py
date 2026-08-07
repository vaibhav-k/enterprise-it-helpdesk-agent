"""
Azure identity provider.

Uses DefaultAzureCredential.

Authentication sources:

Development:
    Azure CLI

Production:
    Managed Identity
"""

from azure.identity import (
    DefaultAzureCredential,
)

credential = DefaultAzureCredential(
    exclude_interactive_browser_credential=True,
)


def get_azure_credential() -> DefaultAzureCredential:
    """
    Return Azure credential provider.

    Returns:
        Azure credential object.
    """

    return credential
