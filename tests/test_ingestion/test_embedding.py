# tests/test_ingestion/test_embedding.py

import numpy as np
import pytest

from ingestion.embedding import Embedder


@pytest.fixture(scope="session")
def embedder():
    """
    Session-scoped embedder to avoid reloading the model for each test.
    """
    return Embedder(
        model_name="BAAI/bge-large-en-v1.5",
        batch_size=4,
        normalize=True,
    )


def test_embed_single_query(embedder):
    query = "What is retrieval augmented generation?"
    embedding = embedder.embed_query(query)

    assert isinstance(embedding, np.ndarray)
    assert embedding.shape == (1024,)
    assert np.isclose(np.linalg.norm(embedding), 1.0, atol=1e-4)


def test_embed_multiple_texts(embedder):
    texts = [
        "Retrieval augmented generation combines search and LLMs.",
        "Embeddings map text into a dense vector space.",
        "FAISS enables efficient similarity search.",
    ]

    embeddings = embedder.embed_texts(texts)

    assert isinstance(embeddings, np.ndarray)
    assert embeddings.shape == (len(texts), 1024)

    # Each embedding should be L2-normalized
    norms = np.linalg.norm(embeddings, axis=1)
    assert np.allclose(norms, 1.0, atol=1e-4)


def test_empty_input(embedder):
    embeddings = embedder.embed_texts([])

    assert isinstance(embeddings, np.ndarray)
    assert embeddings.shape[0] == 0
