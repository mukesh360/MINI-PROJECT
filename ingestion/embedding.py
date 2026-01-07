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

        self.model = SentenceTransformer(
            model_name,
            device=self.device,
            trust_remote_code=True,
        )

        self.dim = self.model.get_sentence_embedding_dimension()

    # -------------------------------------------------
    # 🔑 CANONICAL EMBEDDING API (DO NOT REMOVE)
    # -------------------------------------------------
    def embed(self, texts: List[str]) -> np.ndarray:
        """
        Canonical embedding API.
        Used by retrieval, FAISS, and tests.
        """
        if not texts:
            return np.empty((0, self.dim), dtype="float32")

        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize,
        )

        return embeddings.astype("float32")

    # -------------------------------------------------
    # Convenience wrappers
    # -------------------------------------------------
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        return self.embed(texts)

    def embed_query(self, query: str) -> np.ndarray:
        embedding = self.model.encode(
            query,
            batch_size=1,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize,
        )

        # Always return shape (D,)
        if embedding.ndim == 2:
            embedding = embedding[0]

        return embedding.astype("float32")



    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Backward-compatible alias for legacy tests.
        DO NOT remove.
        """
        return self.embed(texts)