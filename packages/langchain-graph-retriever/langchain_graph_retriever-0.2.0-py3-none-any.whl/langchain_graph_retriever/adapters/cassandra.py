from typing import (
    Any,
    List,
    Sequence,
    override,
)

try:
    from langchain_community.vectorstores import Cassandra
except (ImportError, ModuleNotFoundError):
    raise ImportError("please `pip install langchain-community cassio`")

from langchain_core.documents import Document

from .base import METADATA_EMBEDDING_KEY, Adapter


class CassandraAdapter(Adapter[Cassandra]):
    """Adapter for Cassandra vector store."""

    def __init__(
        self,
        vector_store: Cassandra,
        *,
        denormalized_path_delimiter: str = ".",
        denormalized_static_value: str = "$",
    ):
        super().__init__(
            vector_store,
            use_normalized_metadata=False,
            denormalized_path_delimiter=denormalized_path_delimiter,
            denormalized_static_value=denormalized_static_value,
        )

    @override
    def similarity_search_with_embedding_by_vector(  # type: ignore
        self,
        embedding: List[float],
        k: int = 4,
        filter: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> List[Document]:
        results = self._similarity_search_with_embedding_id_by_vector(
            embedding=embedding,
            k=k,
            filter=filter,
            **kwargs,
        )
        docs: List[Document] = []
        for doc, embedding, id in results:
            doc.metadata[METADATA_EMBEDDING_KEY] = embedding
            doc.id = id
            docs.append(doc)
        return docs

    def _similarity_search_with_embedding_id_by_vector(
        self,
        embedding: list[float],
        k: int = 4,
        filter: dict[str, str] | None = None,
        body_search: str | list[str] | None = None,
    ) -> list[tuple[Document, list[float], str]]:
        """Return docs most similar to embedding vector.

        Args:
            embedding: Embedding to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.
            filter: Filter on the metadata to apply.
            body_search: Document textual search terms to apply.
                Only supported by Astra DB at the moment.

        Returns
        -------
            List of (Document, embedding, id), the most similar to the query vector.

        """
        kwargs: dict[str, Any] = {}
        if filter is not None:
            kwargs["metadata"] = filter
        if body_search is not None:
            kwargs["body_search"] = body_search

        if k == 0:
            return []

        hits = self.vector_store.table.ann_search(
            vector=embedding,
            n=k,
            **kwargs,
        )
        return [
            (
                self.vector_store._row_to_document(row=hit),
                hit["vector"],
                hit["row_id"],
            )
            for hit in hits
        ]

    @override
    async def asimilarity_search_with_embedding(
        self,
        query: str,
        k: int = 4,
        filter: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> tuple[list[float], list[Document]]:
        query_embedding = self._safe_embedding.embed_query(text=query)
        if k == 0:
            return query_embedding, []

        docs = await self.asimilarity_search_with_embedding_by_vector(
            embedding=query_embedding,
            k=k,
            filter=filter,
            **kwargs,
        )
        return query_embedding, docs

    @override
    async def asimilarity_search_with_embedding_by_vector(  # type: ignore
        self, **kwargs: Any
    ) -> list[Document]:
        results = (
            await self.vector_store.asimilarity_search_with_embedding_id_by_vector(
                **kwargs
            )
        )
        docs: List[Document] = []
        for doc, embedding, id in results:
            doc.metadata[METADATA_EMBEDDING_KEY] = embedding
            doc.id = id
            docs.append(doc)
        return docs

    @override
    def get(self, ids: Sequence[str], /, **kwargs: Any) -> list[Document]:
        """Get documents by id."""
        docs: list[Document] = []
        for id in ids:
            doc = self._get_by_document_id(id)
            if doc is not None:
                docs.append(doc)
        return docs

    def _get_by_document_id(self, id: str) -> Document | None:
        row = self.vector_store.table.get(row_id=id)
        if row is None:
            return None
        return Document(
            id=row["row_id"],
            page_content=row["body_blob"],
            metadata={
                METADATA_EMBEDDING_KEY: row["vector"],
                **row["metadata"],
            },
        )

    @override
    async def aget(self, ids: Sequence[str], /, **kwargs: Any) -> list[Document]:
        """Get documents by id."""
        docs: list[Document] = []
        for id in ids:
            doc = await self._aget_by_document_id(id, **kwargs)
            if doc is not None:
                docs.append(doc)
        return docs

    async def _aget_by_document_id(self, id: str) -> Document | None:
        row = await self.vector_store.table.aget(row_id=id)
        if row is None:
            return None
        return Document(
            id=row["row_id"],
            page_content=row["body_blob"],
            metadata={
                METADATA_EMBEDDING_KEY: row["vector"],
                **row["metadata"],
            },
        )
