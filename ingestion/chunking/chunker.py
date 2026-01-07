from typing import List, Union
from ingestion.chunking.token_chunker import TokenChunker


def chunk_text(
    text: Union[str, List[str]],
    max_tokens: int = 300,
    overlap: int = 100,
) -> List[str]:
    """
    Safely chunk text into token-bounded chunks.

    Handles:
    - empty input
    - list[str]
    - excessive whitespace
    - short text
    """

    if not text:
        return []

    # Normalize input
    if isinstance(text, list):
        text = "\n".join(t for t in text if isinstance(t, str) and t.strip())

    if not isinstance(text, str):
        raise TypeError(f"Expected str or list[str], got {type(text)}")

    text = text.strip()
    if not text:
        return []

    chunker = TokenChunker(
        max_tokens=max_tokens,
        overlap=overlap,
    )

    chunks = chunker.chunk(text)

    # Final sanitation
    return [c.strip() for c in chunks if c.strip()]
