# retrieval/pipeline.py

from retrieval.retriever import Retriever
from retrieval.context_builder import build_context_from_chunks
from storage.registry import load_all_chunks

class RetrievalPipeline:
    def __init__(self):
        chunks = load_all_chunks()
        self.retriever = Retriever(chunks)

    def get_context(self, query: str, max_chunks=5):
        retrieved = self.retriever.retrieve(query, max_chunks)
        return build_context_from_chunks(retrieved)
