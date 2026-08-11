"""
Tests for the enterprise knowledge service.
"""

from unittest.mock import MagicMock, patch

import pytest

from app.models.knowledge import KnowledgeContext
from app.services.knowledge_service import KnowledgeService


def test_knowledge_service_requires_storage_account() -> None:
    """Verify storage account configuration is required."""

    with patch(
        "app.services.knowledge_service.settings.azure_storage_account",
        "",
    ):
        with patch(
            "app.services.knowledge_service.settings.azure_container",
            "knowledge-base",
        ):
            with pytest.raises(
                ValueError,
                match="AZURE_STORAGE_ACCOUNT must be configured",
            ):
                KnowledgeService()


def test_knowledge_service_requires_container() -> None:
    """Verify storage container configuration is required."""

    with patch(
        "app.services.knowledge_service.settings.azure_storage_account",
        "storage-account",
    ):
        with patch(
            "app.services.knowledge_service.settings.azure_container",
            "",
        ):
            with pytest.raises(
                ValueError,
                match="AZURE_CONTAINER must be configured",
            ):
                KnowledgeService()


def test_build_account_url_from_account_name() -> None:
    """Verify storage account URL construction via initialization."""
    with patch(
        "app.services.knowledge_service.settings.azure_storage_account",
        "helpdeskstorage",
    ):
        with patch(
            "app.services.knowledge_service.settings.azure_container",
            "knowledge-base",
        ):
            with patch(
                "app.services.knowledge_service.DefaultAzureCredential",
            ):
                with patch(
                    "app.services.knowledge_service.BlobServiceClient",
                ):
                    service = KnowledgeService()
                    # Access internal client base URL indirectly via expected behavior
                    assert service.build_account_url("helpdeskstorage") == (
                        "https://helpdeskstorage.blob.core.windows.net"
                    )


def test_build_account_url_preserves_https_url() -> None:
    """Verify an existing HTTPS endpoint is preserved."""

    result = KnowledgeService.build_account_url(
        "https://example.blob.core.windows.net/",
    )

    assert result == ("https://example.blob.core.windows.net")


def test_empty_query_returns_empty_context() -> None:
    """Verify an empty query does not access Azure."""

    with patch(
        "app.services.knowledge_service.settings.azure_storage_account",
        "storage-account",
    ):
        with patch(
            "app.services.knowledge_service.settings.azure_container",
            "knowledge-base",
        ):
            with patch(
                "app.services.knowledge_service.DefaultAzureCredential",
            ):
                with patch(
                    "app.services.knowledge_service.BlobServiceClient",
                ) as mock_client:
                    service = KnowledgeService()

                    result = service.get_context("   ")

    assert result == KnowledgeContext()
    mock_client.assert_called_once()


def test_get_context_returns_matching_document() -> None:
    """Verify keyword matching returns a relevant document."""

    blob_service = MagicMock()
    container_client = MagicMock()
    blob_client = MagicMock()

    blob_service.get_container_client.return_value = container_client

    blob = MagicMock()
    blob.name = "vpn-troubleshooting.txt"
    blob.size = 100

    container_client.list_blobs.return_value = [blob]

    container_client.get_blob_client.return_value = blob_client

    blob_client.download_blob.return_value.readall.return_value = (
        b"VPN troubleshooting guide. Check the VPN client and network connection."
    )

    with patch(
        "app.services.knowledge_service.settings.azure_storage_account",
        "storage-account",
    ):
        with patch(
            "app.services.knowledge_service.settings.azure_container",
            "knowledge-base",
        ):
            with patch(
                "app.services.knowledge_service.DefaultAzureCredential",
            ):
                with patch(
                    "app.services.knowledge_service.BlobServiceClient",
                    return_value=blob_service,
                ):
                    service = KnowledgeService()

                    result = service.get_context(
                        "VPN troubleshooting",
                    )

    assert len(result.documents) == 1
    assert result.documents[0].content.startswith(
        "VPN troubleshooting guide",
    )


def test_get_context_returns_empty_for_no_match() -> None:
    """Verify unmatched queries return empty context."""

    blob_service = MagicMock()
    container_client = MagicMock()

    blob_service.get_container_client.return_value = container_client

    blob = MagicMock()
    blob.name = "printer-guide.txt"
    blob.size = 100

    container_client.list_blobs.return_value = [blob]

    container_client.get_blob_client.return_value = MagicMock()

    blob_client = container_client.get_blob_client.return_value

    blob_client.download_blob.return_value.readall.return_value = (
        b"Printer installation and troubleshooting guide."
    )

    with patch(
        "app.services.knowledge_service.settings.azure_storage_account",
        "storage-account",
    ):
        with patch(
            "app.services.knowledge_service.settings.azure_container",
            "knowledge-base",
        ):
            with patch(
                "app.services.knowledge_service.DefaultAzureCredential",
            ):
                with patch(
                    "app.services.knowledge_service.BlobServiceClient",
                    return_value=blob_service,
                ):
                    service = KnowledgeService()

                    result = service.get_context(
                        "password reset",
                    )

    assert result == KnowledgeContext()


def test_get_context_respects_max_documents() -> None:
    """Verify retrieval does not exceed the document limit."""

    blob_service = MagicMock()
    container_client = MagicMock()

    blob_service.get_container_client.return_value = container_client

    def make_blob(name: str) -> MagicMock:
        """Create a mock blob with a real ``name`` attribute."""

        blob = MagicMock()
        blob.name = name
        blob.size = 100
        return blob

    container_client.list_blobs.return_value = [
        make_blob("vpn-1.txt"),
        make_blob("vpn-2.txt"),
        make_blob("vpn-3.txt"),
    ]

    def get_blob_client(
        name: str,
    ) -> MagicMock:
        """Return a mock blob client for a blob name."""

        blob_client = MagicMock()

        blob_client.download_blob.return_value.readall.return_value = (
            f"VPN troubleshooting information for {name}".encode()
        )

        return blob_client

    container_client.get_blob_client.side_effect = get_blob_client

    with patch(
        "app.services.knowledge_service.settings.azure_storage_account",
        "storage-account",
    ):
        with patch(
            "app.services.knowledge_service.settings.azure_container",
            "knowledge-base",
        ):
            with patch(
                "app.services.knowledge_service.DefaultAzureCredential",
            ):
                with patch(
                    "app.services.knowledge_service.BlobServiceClient",
                    return_value=blob_service,
                ):
                    service = KnowledgeService()

                    result = service.get_context(
                        "VPN troubleshooting",
                        max_documents=2,
                    )

    assert len(result.documents) == 2
