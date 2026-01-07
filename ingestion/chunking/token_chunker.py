from typing import List
from ingestion.chunking.tokenizer import TokenCounter


class TokenChunker:
    """
    Token-based text chunker with overlap.

    Guarantees:
    - No chunk exceeds max_tokens
    - Deterministic output
    - Overlap preserved
    - Empty-safe
    """

    def __init__(
        self,
        max_tokens: int = 512,
        overlap: int = 50,
        tokenizer_name: str = "bert-base-uncased",
    ):
        if overlap >= max_tokens:
            raise ValueError("overlap must be smaller than max_tokens")

        self.max_tokens = max_tokens
        self.overlap = overlap
        self.tokenizer = TokenCounter(tokenizer_name)

    def chunk(self, text: str) -> List[str]:
        """
        Split text into overlapping token-based chunks.
        """

        if not text or not text.strip():
            return []

        tokens = self.tokenizer.encode(text)

        if len(tokens) <= self.max_tokens:
            return [text.strip()]

        chunks: List[str] = []
        start = 0

        while start < len(tokens):
            end = start + self.max_tokens
            token_slice = tokens[start:end]

            chunk_text = self.tokenizer.decode(token_slice)
            chunk_text = chunk_text.strip()

            if chunk_text:
                chunks.append(chunk_text)

            # move window
            start += self.max_tokens - self.overlap

        return chunks
