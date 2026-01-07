# retrieval/confidence.py

from typing import List, Dict


class ConfidenceGate:
    def __init__(
        self,
        score_threshold: float = 0.35,
        min_chunks: int = 2,
        refusal_message: str = "Not found in documents",
    ):
        self.score_threshold = score_threshold
        self.min_chunks = min_chunks
        self.refusal_message = refusal_message

    def filter_chunks(self, results: List[Dict]) -> List[Dict]:
        """
        Filters chunks by confidence threshold.
        Each result must contain: {chunk_id, score, text}
        """
        strong = [
            r for r in results
            if r["score"] >= self.score_threshold
        ]

        return strong

    def should_refuse(self, strong_chunks: List[Dict]) -> bool:
        return len(strong_chunks) < self.min_chunks

    def refusal_response(self) -> str:
        return self.refusal_message
