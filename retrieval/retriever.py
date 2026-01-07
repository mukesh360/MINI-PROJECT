import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self, chunks, model_name="all-MiniLM-L6-v2"):
        """
        chunks: List[str] → text chunks from PDF
        """
        self.chunks = chunks
        self.embedder = SentenceTransformer(model_name)

        embeddings = self.embedder.encode(
            chunks, show_progress_bar=True
        )

        embeddings = np.array(embeddings).astype("float32")
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def retrieve(self, query, top_k=3):
        query_vec = self.embedder.encode([query]).astype("float32")
        distances, indices = self.index.search(query_vec, top_k)

        return [self.chunks[i] for i in indices[0]]
