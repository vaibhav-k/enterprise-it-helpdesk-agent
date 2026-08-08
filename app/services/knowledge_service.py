"""
Enterprise knowledge retrieval service.

Provides a small application-level abstraction over Azure Blob Storage
with application-level security and context-size limits.
"""

from __future__ import annotations

import re

from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from app.core.config import settings
from app.models.knowledge import KnowledgeContext, KnowledgeDocument


class KnowledgeService:
    """Retrieve enterprise IT knowledge from Azure Blob Storage."""

    def __init__(self) -> None:
        """Initialize the Azure Blob Storage client."""

        account = settings.azure_storage_account.strip()
        container = settings.azure_container.strip()

        if not account:
            raise ValueError(
                "AZURE_STORAGE_ACCOUNT must be configured.",
            )

        if not container:
            raise ValueError(
                "AZURE_CONTAINER must be configured.",
            )

        credential = DefaultAzureCredential()

        account_url = self.build_account_url(account)

        self._client = BlobServiceClient(
            account_url=account_url,
            credential=credential,
        )

        self._container = container

    @staticmethod
    def build_account_url(account: str) -> str:
        """
        Build the Azure Blob Storage account URL.

        Args:
            account: Storage account name or URL.

        Returns:
            Normalized Blob Storage account URL.
        """

        normalized = account.strip().rstrip("/")

        if not normalized:
            raise ValueError(
                "Azure storage account cannot be empty.",
            )

        if normalized.startswith("https://"):
            return normalized

        return f"https://{normalized}.blob.core.windows.net"

    @staticmethod
    def _extract_query_terms(
        query: str,
    ) -> set[str]:
        """
        Extract meaningful search terms from a query.

        Args:
            query: User's helpdesk question.

        Returns:
            Normalized query terms.
        """

        return {
            term
            for term in re.findall(
                r"\b[a-z0-9]+\b",
                query.lower(),
            )
            if len(term) >= 3
        }

    @staticmethod
    def _matches_query(
        blob_name: str,
        content: str,
        query_terms: set[str],
    ) -> bool:
        """
        Determine whether a document matches the query.

        Args:
            blob_name: Blob name.
            content: Blob content.
            query_terms: Normalized query terms.

        Returns:
            True when at least one query term matches.
        """

        if not query_terms:
            return False

        searchable_text = (f"{blob_name} {content}").lower()

        document_terms = set(
            re.findall(
                r"\b[a-z0-9]+\b",
                searchable_text,
            ),
        )

        return bool(
            query_terms.intersection(document_terms),
        )

    @staticmethod
    def _truncate_content(
        content: str,
        remaining_chars: int,
    ) -> str:
        """
        Limit document content to the remaining context budget.

        Args:
            content: Document content.
            remaining_chars: Available context characters.

        Returns:
            Content limited to the available budget.
        """

        if remaining_chars <= 0:
            return ""

        return content[:remaining_chars]

    def get_context(
        self,
        query: str,
        *,
        max_documents: int = 5,
    ) -> KnowledgeContext:
        """
        Retrieve knowledge documents relevant to a query.

        Retrieval currently performs a simple filename/content keyword
        match. Semantic retrieval can be introduced later.

        Security limits are applied before content is returned:

        - Maximum number of documents.
        - Maximum size of each document.
        - Maximum combined context size.

        Retrieved content is reference material only. This service does
        not treat document content as application instructions.

        Args:
            query: User's helpdesk question.
            max_documents: Maximum number of documents to return.

        Returns:
            Matching knowledge context.

        Raises:
            ValueError: If max_documents is invalid.
            RuntimeError: If Azure Blob Storage access fails.
        """

        if max_documents < 1:
            raise ValueError(
                "max_documents must be greater than zero.",
            )

        normalized_query = query.strip()

        if not normalized_query:
            return KnowledgeContext()

        query_terms = self._extract_query_terms(
            normalized_query,
        )

        if not query_terms:
            return KnowledgeContext()

        container_client = self._client.get_container_client(
            self._container,
        )

        documents: list[KnowledgeDocument] = []

        max_document_chars = max(
            1,
            settings.knowledge_max_document_chars,
        )

        max_context_chars = max(
            1,
            settings.knowledge_max_context_chars,
        )

        total_context_chars = 0

        try:
            for blob in container_client.list_blobs():
                if len(documents) >= min(
                    max_documents,
                    settings.knowledge_max_documents,
                ):
                    break

                blob_size = blob.size

                if blob_size and blob_size > max_document_chars:
                    continue

                blob_client = container_client.get_blob_client(
                    blob.name,
                )

                raw_content = blob_client.download_blob().readall()

                content = raw_content.decode(
                    "utf-8",
                    errors="replace",
                )

                if not content.strip():
                    continue

                if not self._matches_query(
                    blob.name,
                    content,
                    query_terms,
                ):
                    continue

                remaining_chars = max_context_chars - total_context_chars

                if remaining_chars <= 0:
                    break

                limited_content = self._truncate_content(
                    content,
                    min(
                        max_document_chars,
                        remaining_chars,
                    ),
                )

                if not limited_content.strip():
                    continue

                documents.append(
                    KnowledgeDocument(
                        name=blob.name,
                        content=limited_content,
                    ),
                )

                total_context_chars += len(
                    limited_content,
                )

        except AzureError as exc:
            raise RuntimeError(
                "Knowledge base retrieval failed.",
            ) from exc

        return KnowledgeContext(
            documents=documents,
        )
