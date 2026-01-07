from retrieval.pipeline import RetrievalPipeline


class FakeDense:
    def search(self, query):
        return [{"chunk_id": "c1", "score": 0.7}]


class FakeSparse:
    def search(self, query):
        return [{"chunk_id": "c2", "score": 0.9}]


class FakeReranker:
    def rerank(self, dense, sparse):
        return dense + sparse


def test_pipeline_combines_dense_sparse(monkeypatch):
    monkeypatch.setattr(
        "retrieval.pipeline.DenseRetriever",
        lambda *a, **k: FakeDense(),
    )
    monkeypatch.setattr(
        "retrieval.pipeline.SparseRetriever",
        lambda *a, **k: FakeSparse(),
    )
    monkeypatch.setattr(
        "retrieval.pipeline.Reranker",
        lambda *a, **k: FakeReranker(),
    )

    pipeline = RetrievalPipeline()
    results = pipeline.search("test")

    assert len(results) == 2
