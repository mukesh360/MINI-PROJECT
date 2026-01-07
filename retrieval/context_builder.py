from typing import List, Tuple
from ingestion.chunking.tokenizer import TokenCounter
from storage.db import get_connection

class ContextBuilder:
    def __init__(self, max_tokens=800):
        self.max_tokens = max_tokens

    def build(self, chunks):
        context = []
        citations = []
        seen = set()

        for c in chunks:
            context.append(c["content"])

            if c["chunk_id"] not in seen:
                citations.append({
                    "chunk_id": c["chunk_id"],
                    "file": c["file_id"],
                    "page": c.get("page", "?")
                })
                seen.add(c["chunk_id"])

        return "\n\n".join(context), citations


def build_context_from_chunks(chunks):
    context_parts = []
    citations = []

    for c in chunks:
        context_parts.append(c["content"])
        citations.append({
            "chunk_id": c["chunk_id"],
            "file": c["file_id"],
            "page": c["page"]
        })

    return "\n\n".join(context_parts), citations


