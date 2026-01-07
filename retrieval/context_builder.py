from typing import List, Tuple
from ingestion.chunking.tokenizer import TokenCounter
from storage.db import get_connection


class ContextBuilder:
    def __init__(self, max_tokens: int = 800):
        self.max_tokens = max_tokens
        self.counter = TokenCounter()

    def build(self, chunks: List[dict]) -> Tuple[str, List[str]]:
        """
        Builds context by:
        - Fetching text from DB
        - Enforcing token budget
        - Returning citations
        """
        conn = get_connection()

        context_parts = []
        citations = []
        total_tokens = 0

        for chunk in chunks:
            chunk_id = chunk["chunk_id"]

            row = conn.execute(
                "SELECT content FROM chunks WHERE chunk_id = ?",
                (chunk_id,),
            ).fetchone()

            if not row:
                continue

            text = row[0]
            tokens = self.counter.count(text)

            if total_tokens + tokens > self.max_tokens:
                break

            context_parts.append(text)
            citations.append(chunk_id)
            total_tokens += tokens

        conn.close()

        return "\n\n".join(context_parts), citations
