from typing import List, Dict, Tuple
from rank_bm25 import BM25Okapi
import pickle
import os


class BM25Index:
    def __init__(self):
        self.bm25: BM25Okapi | None = None
        self.id_map: Dict[int, str] = {}

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """
        Simple, deterministic tokenizer.
        Must match ingestion chunk normalization.
        """
        return text.lower().split()

    def build(self, chunk_ids: List[str], texts: List[str]):
        assert len(chunk_ids) == len(texts), "Chunk IDs and texts mismatch"

        tokenized_corpus = [self._tokenize(t) for t in texts]
        self.bm25 = BM25Okapi(tokenized_corpus)
        self.id_map = {i: cid for i, cid in enumerate(chunk_ids)}

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        assert self.bm25 is not None, "BM25 index not built"

        tokens = self._tokenize(query)
        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True,
        )[:top_k]

        return [(self.id_map[i], float(score)) for i, score in ranked]

    def save(self, index_path: str):
        index_dir = os.path.dirname(index_path)
        if index_dir:
            os.makedirs(index_dir, exist_ok=True)


        with open(index_path, "wb") as f:
            pickle.dump(
                {
                    "bm25": self.bm25,
                    "id_map": self.id_map,
                },
                f,
            )

    @classmethod
    def load(cls, index_path: str) -> "BM25Index":
        with open(index_path, "rb") as f:
            data = pickle.load(f)

        obj = cls()
        obj.bm25 = data["bm25"]
        obj.id_map = data["id_map"]
        return obj

class SparseRetriever:
    def __init__(
        self,
        index_path: str = "bm25.pkl",
        top_k: int = 5,
    ):
        self.index_path = index_path
        self.top_k = top_k
        self.index = BM25Index.load(index_path)

    def search(self, query: str):
        results = self.index.search(query, top_k=self.top_k)

        return [
            {
                "chunk_id": cid,
                "score": score,
                "source": "sparse",
            }
            for cid, score in results
        ]
