import abc
from typing import Callable, Generic, TypeVar

import pytest
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_graph_retriever.adapters import Adapter
from langchain_graph_retriever.document_transformers.metadata_denormalizer import (
    MetadataDenormalizer,
)

ALL_STORES = ["mem_norm", "mem", "astra", "cassandra", "chroma", "opensearch"]
TESTCONTAINER_STORES = ["cassandra", "opensearch"]


@pytest.fixture(scope="session")
def enabled_stores(request: pytest.FixtureRequest) -> set[str]:
    # TODO: Use StrEnum?
    stores = request.config.getoption("--stores")

    if stores and "all" in stores:
        return set(ALL_STORES)
    elif stores:
        return set(stores)
    else:
        return {"mem_norm", "mem"}


def use_testcontainer(request: pytest.FixtureRequest, store: str) -> bool:
    testcontainers = request.config.getoption("--testcontainer")
    if testcontainers and "none" in testcontainers:
        return False
    elif testcontainers:
        return store in testcontainers
    else:
        return True


@pytest.fixture(scope="session", params=ALL_STORES)
def store_param(request: pytest.FixtureRequest, enabled_stores: set[str]) -> str:
    store: str = request.param
    if store not in enabled_stores:
        pytest.skip(f"'{store}' is not enabled")
    return store


T = TypeVar("T", bound=VectorStore)


class StoreFactory(abc.ABC, Generic[T]):
    def __init__(
        self,
        create_store: Callable[[str, list[Document], Embeddings], T],
        create_adapter: Callable[[T], Adapter],
        teardown: Callable[[T], None] | None = None,
    ):
        self._create_store = create_store
        self._create_adapter = create_adapter
        self._teardown = teardown
        self._index = 0

    def create(
        self,
        request: pytest.FixtureRequest,
        embedding: Embeddings,
        docs: list[Document],
    ) -> Adapter:
        name = f"test_{self._index}"
        self._index += 1
        store = self._create_store(name, docs, embedding)

        if self._teardown is not None:
            # make a local copy of the non-None teardown. This makes `mypy` happy.
            # Otherwise, it (correctly) recognizes that `self._teardown` could be not
            # `None` and `None` later (when the finalizer is called)
            teardown = self._teardown
            request.addfinalizer(lambda: teardown(store))

        return self._create_adapter(store)


def _cassandra_store_factory(request: pytest.FixtureRequest):
    import os

    from cassandra.cluster import Cluster  # type: ignore
    from langchain_community.vectorstores.cassandra import Cassandra
    from langchain_graph_retriever.adapters.cassandra import (
        CassandraAdapter,
    )

    if use_testcontainer(request, "cassandra"):
        from testcontainers.cassandra import CassandraContainer  # type: ignore

        container = CassandraContainer()
        container.start()
        request.addfinalizer(lambda: container.stop())
        contact_points = container.get_contact_points()
    elif "CASSANDRA_CONTACT_POINTS" in os.environ:
        contact_points = [
            cp.strip()
            for cp in os.environ["CASSANDRA_CONTACT_POINTS"].split(",")
            if cp.strip()
        ]
    else:
        contact_points = None

    cluster = Cluster(contact_points)
    session = cluster.connect()

    KEYSPACE = "graph_test_keyspace"
    session.execute(
        (
            f"CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}"
            " WITH replication = "
            "{'class': 'SimpleStrategy', 'replication_factor': 1}"
        )
    )

    request.addfinalizer(lambda: cluster.shutdown())

    def create_cassandra(
        name: str, docs: list[Document], embedding: Embeddings
    ) -> Cassandra:
        session = cluster.connect()
        session.execute(f"DROP TABLE IF EXISTS {KEYSPACE}.{name}")

        store = Cassandra(
            embedding=embedding,
            session=session,
            keyspace=KEYSPACE,
            table_name=name,
        )
        docs = list(MetadataDenormalizer().transform_documents(docs))
        store.add_documents(docs)
        return store

    def teardown_cassandra(cassandra: Cassandra):
        assert cassandra.session is not None
        cassandra.session.shutdown()

    return StoreFactory[Cassandra](
        create_store=create_cassandra,
        create_adapter=CassandraAdapter,
        teardown=teardown_cassandra,
    )


def _opensearch_store_factory(request: pytest.FixtureRequest):
    from langchain_community.vectorstores import OpenSearchVectorSearch
    from langchain_graph_retriever.adapters.open_search import (
        OpenSearchAdapter,
    )

    if use_testcontainer(request, "opensearch"):
        from testcontainers.opensearch import OpenSearchContainer  # type: ignore

        # If the admin password doesn't pass the length and regex requirements
        # starting the container will hang (`docker ps <container_id>` to debug).
        container = OpenSearchContainer(
            image="opensearchproject/opensearch:2.18.0",
            initial_admin_password="SomeRandomP4ssword",
        )
        container.start()
        request.addfinalizer(lambda: container.stop())

        config = container.get_config()
        opensearch_url = f"http://{config['host']}:{config['port']}"
        kwargs = {"http_auth": (config["username"], config["password"])}
    else:
        opensearch_url = "http://localhost:9200"
        kwargs = {}

    def create_open_search(
        name: str, docs: list[Document], embedding: Embeddings
    ) -> OpenSearchVectorSearch:
        store = OpenSearchVectorSearch(
            opensearch_url=opensearch_url,
            index_name=name,
            embedding_function=embedding,
            engine="faiss",
            **kwargs,
        )
        store.add_documents(docs)
        return store

    def teardown_open_search(store: OpenSearchVectorSearch) -> None:
        if store.index_exists():
            store.delete_index()

    return StoreFactory[OpenSearchVectorSearch](
        create_store=create_open_search,
        create_adapter=OpenSearchAdapter,
        teardown=teardown_open_search,
    )


def _astra_store_factory(_request: pytest.FixtureRequest) -> StoreFactory:
    import os

    from astrapy import AstraDBDatabaseAdmin
    from astrapy.authentication import StaticTokenProvider
    from dotenv import load_dotenv
    from langchain_astradb import AstraDBVectorStore
    from langchain_graph_retriever.adapters.astra import (
        AstraAdapter,
    )

    load_dotenv()

    token = StaticTokenProvider(os.environ["ASTRA_DB_APPLICATION_TOKEN"])
    keyspace = os.environ.get("ASTRA_DB_KEYSPACE", "default_keyspace")
    api_endpoint = os.environ["ASTRA_DB_API_ENDPOINT"]

    admin = AstraDBDatabaseAdmin(api_endpoint=api_endpoint, token=token)
    admin.create_keyspace(keyspace)

    def create_astra(
        name: str, docs: list[Document], embedding: Embeddings
    ) -> AstraDBVectorStore:
        try:
            from langchain_astradb import AstraDBVectorStore

            store = AstraDBVectorStore(
                embedding=embedding,
                collection_name=name,
                namespace=keyspace,
                token=token,
                api_endpoint=api_endpoint,
            )
            store.add_documents(docs)
            return store

        except (ImportError, ModuleNotFoundError):
            msg = (
                "to test graph-traversal with AstraDB, please"
                " install langchain-astradb and python-dotenv"
            )
            raise ImportError(msg)

    def teardown_astra(store: AstraDBVectorStore):
        store.delete_collection()

    return StoreFactory[AstraDBVectorStore](
        create_store=create_astra,
        create_adapter=AstraAdapter,
        teardown=teardown_astra,
    )


def _in_memory_store_factory(
    _request: pytest.FixtureRequest, use_normalized_metadata: bool
) -> StoreFactory:
    from langchain_core.vectorstores import InMemoryVectorStore
    from langchain_graph_retriever.adapters.in_memory import (
        InMemoryAdapter,
    )

    def create_in_memory(
        _name: str, docs: list[Document], emb: Embeddings
    ) -> InMemoryVectorStore:
        if not use_normalized_metadata:
            docs = list(MetadataDenormalizer().transform_documents(docs))
        return InMemoryVectorStore.from_documents(docs, emb)

    return StoreFactory[InMemoryVectorStore](
        create_store=create_in_memory,
        create_adapter=lambda store: InMemoryAdapter(
            store, use_normalized_metadata=use_normalized_metadata
        ),
    )


def _chroma_store_factory(_request: pytest.FixtureRequest) -> StoreFactory:
    from langchain_chroma.vectorstores import Chroma
    from langchain_graph_retriever.adapters.chroma import (
        ChromaAdapter,
    )

    def create_chroma(name: str, docs: list[Document], emb: Embeddings) -> Chroma:
        docs = list(MetadataDenormalizer().transform_documents(docs))
        return Chroma.from_documents(docs, emb, collection_name=name)

    return StoreFactory[Chroma](
        create_store=create_chroma,
        create_adapter=ChromaAdapter,
        teardown=lambda store: store.delete_collection(),
    )


@pytest.fixture(scope="session")
def store_factory(store_param: str, request: pytest.FixtureRequest) -> StoreFactory:
    if store_param == "mem_norm":
        return _in_memory_store_factory(request, use_normalized_metadata=True)
    elif store_param == "mem":
        return _in_memory_store_factory(request, use_normalized_metadata=False)
    elif store_param == "chroma":
        return _chroma_store_factory(request)
    elif store_param == "astra":
        return _astra_store_factory(request)
    elif store_param == "cassandra":
        return _cassandra_store_factory(request)
    elif store_param == "opensearch":
        return _opensearch_store_factory(request)
    else:
        pytest.fail(f"Unsupported store: {store_param}")
