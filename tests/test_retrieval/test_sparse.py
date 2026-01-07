import tempfile
from retrieval.sparse import BM25Index, SparseRetriever


def test_bm25_build_and_search():
    index = BM25Index()

    chunk_ids = ["c1", "c2", "c3"]
    texts = [
        "retrieval augmented generation",
        "bm25 sparse retrieval",
        "vector search faiss",
    ]

    index.build(chunk_ids, texts)

    results = index.search("bm25 retrieval", top_k=2)

    assert len(results) == 2
    assert results[0][0] in chunk_ids
    assert results[0][1] > 0


def test_sparse_retriever_load_and_search(tmp_path):
    index_path = tmp_path / "bm25.pkl"

    index = BM25Index()
    index.build(
        ["c1", "c2"],
        ["hello world", "semantic search"],
    )
    index.save(str(index_path))

    retriever = SparseRetriever(str(index_path), top_k=1)
    results = retriever.search("hello")

    assert len(results) == 1
    assert results[0]["chunk_id"] == "c1"
    assert results[0]["score"] >= 0
