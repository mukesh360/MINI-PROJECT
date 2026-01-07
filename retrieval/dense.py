import json
import faiss
import numpy as np
from typing import List, Dict

from ingestion.embedding import Embedder


class DenseRetriever:
    def __init__(
        self,
        index_path: str,
        mapping_path: str,
        model_name: str = "BAAI/bge-small-en-v1.5",
        top_k: int = 10,
    ):
        self.index = faiss.read_index(index_path)

        with open(mapping_path, "r", encoding="utf-8") as f:
            self.id_map = json.load(f)

        self.embedder = Embedder(model_name=model_name)
        self.top_k = top_k

    def search(self, query: str):
        query_vec = self.embedder.encode([query])  # (1, D)
        scores, indices = self.index.search(query_vec, self.top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            meta = self.id_map[str(idx)]
            results.append({
                "chunk_id": meta["chunk_id"],
                "file_id": meta["file_id"],
                "chunk_index": meta["chunk_index"],
                "score": float(score),
                "source": "dense",
            })
        return results
