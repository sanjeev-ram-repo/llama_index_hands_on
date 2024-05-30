from llama_index.core import SimpleDirectoryReader
from llama_index.core.extractors import SummaryExtractor
from llama_index.core.ingestion import IngestionCache, IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.schema import TextNode
from llama_index.embeddings.gemini import GeminiEmbedding
from logg import log_action
from settings import CACHE_FILE, GEMINI_LLM, STORAGE_PATH


def ingest_documents() -> TextNode:
    """Ingesting documents from the inputs."""
    try:
        documents = SimpleDirectoryReader(STORAGE_PATH, filename_as_id=True).load_data()
        for doc in documents:
            log_action(f"File {doc.id_} uploaded", action_type="UPLOAD")
        try:
            cached_hashes = IngestionCache.from_persist_path(CACHE_FILE)
            print("Cache file found")
        except Exception:
            cached_hashes = ""
            print("No cache found")
        pipeline = IngestionPipeline(
            transformations=[
                TokenTextSplitter(chunk_size=1024, chunk_overlap=256),
                SummaryExtractor(
                    summaries=["self"], GEMINI_LLM=GEMINI_LLM
                ),  # current node summary only
                GeminiEmbedding(),
            ],
            cache=cached_hashes,
        )
        nodes = pipeline.run(documents=documents)
        pipeline.cache.persist(CACHE_FILE)

        return nodes
    except Exception as e:
        raise Exception(f"Unable to transform documents: {str(e)}")


if __name__ == "__main__":
    embedded_nodes = ingest_documents()
