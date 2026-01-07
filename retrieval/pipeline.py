from retrieval.retriever import Retriever
from retrieval.context_builder import build_context_from_chunks
from storage.registry import load_all_chunks


class RetrievalPipeline:
    def __init__(self):
        print("🔧 Initializing RetrievalPipeline")

        chunks = load_all_chunks()

        if not chunks:
            raise RuntimeError(
                "No chunks found. Upload documents before querying."
            )

        self.retriever = Retriever(chunks)

    def get_context(self, query: str, max_chunks: int = 5) -> str:
        retrieved_chunks = self.retriever.retrieve(
            query=query,
            top_k=max_chunks
        )

        return build_context_from_chunks(retrieved_chunks)
