import json
import numpy as np
import faiss
import tempfile
from retrieval.dense import DenseRetriever


def test_dense_retrieval_returns_results(tmp_path, monkeypatch):
    # --- create fake FAISS index ---
    dim = 3
    index = faiss.IndexFlatIP(dim)
    vectors = np.array([
        [1.0, 0.0, 0.0],
        [0.9, 0.1, 0.0],
    ], dtype="float32")
    faiss.normalize_L2(vectors)
    index.add(vectors)

    index_path = tmp_path / "test.faiss"
    faiss.write_index(index, str(index_path))

    # --- mapping ---
    mapping = {
        "0": {"chunk_id": "c1", "file_id": "f1", "chunk_index": 0},
        "1": {"chunk_id": "c2", "file_id": "f1", "chunk_index": 1},
    }
    mapping_path = tmp_path / "map.json"
    mapping_path.write_text(json.dumps(mapping))

    # --- mock embedder ---
    def fake_embed(self, texts):
        return vectors[:1]

    monkeypatch.setattr("ingestion.embedding.Embedder.encode", fake_embed)

    retriever = DenseRetriever(
        index_path=str(index_path),
        mapping_path=str(mapping_path),
        top_k=2,
    )

    results = retriever.search("test query")

    assert len(results) == 2
    assert results[0]["chunk_id"] == "c1"
    assert results[0]["score"] > 0
