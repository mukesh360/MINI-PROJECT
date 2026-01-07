# retrieval/context_builder.py

from typing import List, Dict
from ingestion.chunking.tokenizer import TokenCounter


class ContextBuilder:
    def __init__(
        self,
        max_tokens: int = 2048,
    ):
        self.max_tokens = max_tokens
        self.token_counter = TokenCounter()

    def build(self, chunks: List[Dict]) -> str:
        """
        Packs chunks until token budget is exhausted.
        Each chunk must contain: {text}
        """
        context_parts = []
        used_tokens = 0

        for chunk in chunks:
            text = chunk["text"]
            tokens = self.token_counter.count(text)

            if used_tokens + tokens > self.max_tokens:
                break

            context_parts.append(text)
            used_tokens += tokens

        return "\n\n".join(context_parts)
