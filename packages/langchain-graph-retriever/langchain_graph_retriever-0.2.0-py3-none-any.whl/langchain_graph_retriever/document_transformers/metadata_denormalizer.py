"""Denormalizer for sequence-based metadata fields."""

from typing import Any, Sequence

from langchain_core.documents import BaseDocumentTransformer, Document


class MetadataDenormalizer(BaseDocumentTransformer):
    """Denormalizes sequence-based metadata fields.

    Certain vector stores do not support storing or searching on metadata fields
    with sequence-based values. This transformer converts sequence-based fields
    into simple metadata values.

    Example:
    -------

    .. code-block:: python

        from langchain_core.documents import Document
        from langchain_community.document_transformers.metadata_denormalizer import (
            MetadataDenormalizer,
        )

        doc = Document(
            page_content="test",
            metadata={"place": ["berlin", "paris"], "topic": ["weather"]},
        )

        de_normalizer = MetadataDenormalizer()

        docs = de_normalizer.transform_documents([doc])

        print(docs[0].metadata)


    .. code-block:: output

        {'place.berlin': True, 'place.paris': True, 'topic.weather': True}

    Args:
        keys: A set of metadata keys to denormalize. If empty, all
            sequence-based fields will be denormalized.
        path_delimiter: The path delimiter to use when building denormalized keys.
        static_value: The value to set on each denormalized key.

    """  # noqa: E501

    def __init__(
        self,
        *,
        keys: set[str] = set(),
        path_delimiter: str = ".",
        static_value: Any = "$",
    ):
        """Create a metadata denormalizing transformation.

        Args:
            keys: The set of keys to denormalize. If empty (default), all metadata
                entries containing a collection will be denormalized.
            path_delimiter: The delimiter to use in the denormalized key between the
                original key and the item value.
            static_value: The value to use the denormalized metadata entries.

        """
        self.keys = keys
        self.path_delimiter = path_delimiter
        self.static_value = static_value

    def transform_documents(
        self, documents: Sequence[Document], **kwargs: Any
    ) -> Sequence[Document]:
        """Denormalizes sequence-based metadata fields."""
        transformed_docs = []
        for document in documents:
            new_doc = Document(id=document.id, page_content=document.page_content)
            for key, value in document.metadata.items():
                is_normalized = isinstance(value, Sequence) and not isinstance(
                    value, (str, bytes)
                )
                should_denormalize = (not self.keys) or (key in self.keys)
                if is_normalized and should_denormalize:
                    for item in value:
                        new_doc.metadata[f"{key}{self.path_delimiter}{item}"] = (
                            self.static_value
                        )
                else:
                    new_doc.metadata[key] = value
            transformed_docs.append(new_doc)

        return transformed_docs
