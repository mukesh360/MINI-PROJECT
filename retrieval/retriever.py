import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self, chunks):
        self.chunks = chunks
        self.texts = [c["content"] for c in chunks]

        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = self.embedder.encode(self.texts).astype("float32")

        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def retrieve(self, query, top_k=5):
        q = self.embedder.encode([query]).astype("float32")
        _, idx = self.index.search(q, top_k)
        return [self.chunks[i] for i in idx[0]]
