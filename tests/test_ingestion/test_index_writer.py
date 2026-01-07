import json
import os
import numpy as np
import faiss
import pytest

from ingestion.index_writer import FaissIndexWriter


@pytest.fixture
def tmp_index_paths(tmp_path):
    """
    Temporary paths for FAISS index + ID map.
    """
    index_path = tmp_path / "test_vectors.faiss"
    mapping_path = tmp_path / "id_map.json"
    return str(index_path), str(mapping_path)


@pytest.fixture(scope="session")
def sample_chunks():
    chunk_ids = [
        "doc1_chunk_0",
        "doc1_chunk_1",
        "doc2_chunk_0",
        "doc2_chunk_1",
    ]

    texts = [
        "Retrieval augmented generation combines LLMs with search.",
        "Embeddings represent text in vector space.",
        "FAISS enables fast similarity search.",
        "BGE models are optimized for retrieval tasks.",
    ]

    return chunk_ids, texts


def test_faiss_index_build_and_save(tmp_index_paths, sample_chunks):
    index_path, mapping_path = tmp_index_paths
    chunk_ids, texts = sample_chunks

    writer = FaissIndexWriter(
        index_path=index_path,
        mapping_path=mapping_path,
        model_name="BAAI/bge-small-en-v1.5",
    )

    # Build FAISS index
    writer.build_index(chunk_ids, texts)

    # ---- 6.3 FAISS Index Creation ----
    assert isinstance(writer.index, faiss.IndexFlatIP)

    # ---- 6.6 EXIT CRITERIA ----
    assert writer.index.ntotal == len(chunk_ids)

    # ---- Save to disk ----
    writer.save()

    assert os.path.exists(index_path)
    assert os.path.exists(mapping_path)


def test_id_mapping_integrity(tmp_index_paths, sample_chunks):
    index_path, mapping_path = tmp_index_paths
    chunk_ids, texts = sample_chunks

    writer = FaissIndexWriter(
        index_path=index_path,
        mapping_path=mapping_path,
    )

    writer.build_index(chunk_ids, texts)
    writer.save()

    with open(mapping_path, "r", encoding="utf-8") as f:
        id_map = json.load(f)

    # ---- 6.4 ID Mapping Store ----
    assert len(id_map) == len(chunk_ids)

    for i, chunk_id in enumerate(chunk_ids):
        assert str(i) in id_map
        assert id_map[str(i)] == chunk_id


def test_loaded_index_matches_mapping(tmp_index_paths, sample_chunks):
    index_path, mapping_path = tmp_index_paths
    chunk_ids, texts = sample_chunks

    writer = FaissIndexWriter(
        index_path=index_path,
        mapping_path=mapping_path,
    )

    writer.build_index(chunk_ids, texts)
    writer.save()

    # Load FAISS index
    index = faiss.read_index(index_path)

    with open(mapping_path, "r", encoding="utf-8") as f:
        id_map = json.load(f)

    # ---- 6.6 EXIT CRITERIA (persisted) ----
    assert index.ntotal == len(id_map)


def test_embeddings_are_normalized(sample_chunks):
    """
    Verify that embeddings are L2-normalized (cosine-ready).
    """
    _, texts = sample_chunks

    writer = FaissIndexWriter(
        index_path=":memory:",
        mapping_path=":memory:",
    )

    embeddings = writer.embedder.embed_texts(texts)

    norms = np.linalg.norm(embeddings, axis=1)
    assert np.allclose(norms, 1.0, atol=1e-4)
