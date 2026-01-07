from transformers import AutoTokenizer
from typing import List


class TokenCounter:
    """
    Lightweight tokenizer wrapper used for:
    - Chunking
    - Context budgeting
    - Token length estimation
    """

    def __init__(self, model_name: str = "bert-base-uncased"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            use_fast=True,
        )

    def encode(self, text: str) -> List[int]:
        """
        Encode text into token IDs.
        """
        if not text or not text.strip():
            return []

        return self.tokenizer.encode(
            text,
            add_special_tokens=False,
        )

    def decode(self, token_ids: List[int]) -> str:
        """
        Decode token IDs back to text.
        """
        if not token_ids:
            return ""

        return self.tokenizer.decode(
            token_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )

    def count(self, text: str) -> int:
        """
        Count number of tokens in text.
        """
        return len(self.encode(text))
