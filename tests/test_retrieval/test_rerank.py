from retrieval.rerank import Reranker


def test_reranker_merges_and_sorts():
    dense = [
        {"chunk_id": "a", "score": 0.8},
        {"chunk_id": "b", "score": 0.5},
    ]
    sparse = [
        {"chunk_id": "b", "score": 1.0},
        {"chunk_id": "c", "score": 0.9},
    ]

    reranker = Reranker(weight_dense=0.7, weight_sparse=0.3)
    ranked = reranker.rerank(dense, sparse)

    assert ranked[0]["chunk_id"] == "b"
    assert ranked[0]["score"] > ranked[1]["score"]
    assert any(r["chunk_id"] == "c" for r in ranked)
