from llama_index.core import (
    StorageContext,
    TreeIndex,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.schema import TextNode
from settings import INDEX_STORAGE


def build_indexes(nodes: TextNode) -> tuple[VectorStoreIndex, TreeIndex]:
    """Build indexes or load indexes using the nodes from the documents.

    Args:
        nodes (TextNode): Nodes from the documents.

    Returns:
        tuple[VectorStoreIndex, TreeIndex]: Returns a treeindex and a vectorindex.
    """
    try:
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE)
        vector_index = load_index_from_storage(
            storage_context=storage_context, index_id="vector"
        )
        tree_index = load_index_from_storage(
            storage_context=storage_context, index_id="tree"
        )
        print("Indices stored from location")
    except Exception:
        print("Cannot load indices from the location")
        storage_context = StorageContext.from_defaults()
        vector_index = VectorStoreIndex(nodes, storage_context=storage_context)
        vector_index.set_index_id("vector")
        tree_index = TreeIndex(nodes, storage_context=storage_context)
        tree_index.set_index_id("tree")
        storage_context.persist(persist_dir=INDEX_STORAGE)
        print("New indexes created and persisted.")
    return vector_index, tree_index
