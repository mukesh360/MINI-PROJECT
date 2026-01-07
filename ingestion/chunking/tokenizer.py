# ingestion/chunking/tokenizer.py

from transformers import AutoTokenizer


class TokenCounter:
    """
    Lightweight token counter for budgeting (NOT chunking).
    """

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            use_fast=True
        )

    def count(self, text: str) -> int:
        if not text:
            return 0
        return len(self.tokenizer.encode(text, add_special_tokens=False))
