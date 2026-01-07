from typing import List, Dict


class Reranker:
    def __init__(self, weight_dense: float = 0.7, weight_sparse: float = 0.3):
        self.w_dense = weight_dense
        self.w_sparse = weight_sparse

    def rerank(
        self,
        dense_results: List[Dict],
        sparse_results: List[Dict],
    ) -> List[Dict]:
        merged = {}

        for r in dense_results:
            merged[r["chunk_id"]] = {
                **r,
                "dense_score": r["score"],
                "sparse_score": 0.0,
            }

        for r in sparse_results:
            if r["chunk_id"] in merged:
                merged[r["chunk_id"]]["sparse_score"] = r["score"]
            else:
                merged[r["chunk_id"]] = {
                    **r,
                    "dense_score": 0.0,
                    "sparse_score": r["score"],
                }

        for v in merged.values():
            v["score"] = (
                self.w_dense * v["dense_score"]
                + self.w_sparse * v["sparse_score"]
            )

        return sorted(merged.values(), key=lambda x: x["score"], reverse=True)
