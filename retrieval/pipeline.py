from typing import List, Dict

from retrieval.dense import DenseRetriever
from retrieval.sparse import SparseRetriever
from retrieval.rerank import Reranker
from storage.db import get_connection


class RetrievalPipeline:
    def __init__(
        self,
        faiss_index_path: str = "vectors.faiss",
        mapping_path: str = "id_map.json",
        dense_top_k: int = 30,     # ⬅ expanded
        sparse_top_k: int = 30,    # ⬅ expanded
    ):
        self.dense = DenseRetriever(
            index_path=faiss_index_path,
            mapping_path=mapping_path,
            top_k=dense_top_k,
        )
        self.sparse = SparseRetriever(top_k=sparse_top_k)
        self.reranker = Reranker()

    def search(self, query: str):
        dense_results = self.dense.search(query)
        sparse_results = self.sparse.search(query)

        ranked = self.reranker.rerank(
            dense_results,
            sparse_results,
        )

        return self._attach_text(ranked)



    def _attach_text(self, results: List[Dict]) -> List[Dict]:
        conn = get_connection()
        enriched = []

        for r in results:
            row = conn.execute(
                """
                SELECT content
                FROM chunks
                WHERE chunk_id = ?
                """,
                (r["chunk_id"],)
            ).fetchone()

            if row:
                r["text"] = row[0]
                enriched.append(r)

        conn.close()
        return enriched
