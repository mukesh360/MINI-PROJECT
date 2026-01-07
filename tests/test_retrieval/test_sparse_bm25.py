import os
import pytest

from retrieval.sparse import BM25Index


@pytest.fixture
def sample_chunks():
    chunk_ids = [
        "doc1_chunk_0",
        "doc1_chunk_1",
        "doc2_chunk_0",
    ]

    texts = [
        "Retrieval augmented generation uses search.",
        "BM25 is a sparse retrieval algorithm.",
        "FAISS handles dense vector search.",
    ]

    return chunk_ids, texts


def test_bm25_build_and_search(sample_chunks):
    chunk_ids, texts = sample_chunks

    bm25 = BM25Index()
    bm25.build(chunk_ids, texts)

    results = bm25.search("sparse retrieval", top_k=2)

    assert len(results) == 2
    assert results[0][0] in chunk_ids
    assert results[0][1] >= results[1][1]


def test_bm25_persistence(tmp_path, sample_chunks):
    chunk_ids, texts = sample_chunks

    bm25 = BM25Index()
    bm25.build(chunk_ids, texts)

    index_path = tmp_path / "bm25.pkl"
    bm25.save(str(index_path))

    assert os.path.exists(index_path)

    loaded = BM25Index.load(str(index_path))

    results = loaded.search("vector search", top_k=1)

    assert len(results) == 1
    assert results[0][0] in chunk_ids
