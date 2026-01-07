# ingestion/embedding.py

from typing import List
import torch
from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:
    """
    Production-ready embedding wrapper for BAAI BGE models.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-large-en-v1.5",
        device: str | None = None,
        batch_size: int = 32,
        normalize: bool = True,
    ):
        self.model_name = model_name
        self.batch_size = batch_size
        self.normalize = normalize

        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device

        # Load model
        self.model = SentenceTransformer(
            model_name,
            device=self.device,
            trust_remote_code=True,
        )

        self.dim = self.model.get_sentence_embedding_dimension()

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.

        Returns:
            np.ndarray: shape (N, D)
        """
        if not texts:
            return np.empty((0, self.model.get_sentence_embedding_dimension()))

        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize,
        )

        return embeddings

    def embed_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a single query.
        """
        embedding = self.model.encode(
            query,
            batch_size=1,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize,
        )
        return embedding
