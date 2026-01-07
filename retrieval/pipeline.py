from retrieval.retriever import Retriever
from retrieval.context_builder import ContextBuilder
from storage.registry import load_all_chunks

class RetrievalPipeline:
    def __init__(self):
        chunks = load_all_chunks()
        if not chunks:
            raise RuntimeError("No documents indexed")

        self.retriever = Retriever(chunks)
        self.context_builder = ContextBuilder()

    def get_context(self, query: str):
        retrieved = self.retriever.retrieve(query)
        return self.context_builder.build(retrieved)
