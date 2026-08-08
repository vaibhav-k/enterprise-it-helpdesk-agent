"""
Knowledge retrieval models.
"""

from pydantic import BaseModel, Field


class KnowledgeDocument(BaseModel):
    """A document retrieved from the enterprise knowledge base."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    content: str = Field(
        ...,
        min_length=1,
        max_length=20_000,
    )


class KnowledgeContext(BaseModel):
    """Knowledge context supplied to the helpdesk agent."""

    documents: list[KnowledgeDocument] = Field(
        default_factory=lambda: list[KnowledgeDocument](),
        max_length=5,
    )
