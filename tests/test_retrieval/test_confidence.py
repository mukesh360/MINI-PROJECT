from retrieval.confidence import ConfidenceGate


def test_refusal_when_scores_low():
    gate = ConfidenceGate()

    results = [
        {"chunk_id": "c1", "score": 0.2, "text": "irrelevant"},
        {"chunk_id": "c2", "score": 0.3, "text": "weak"},
    ]

    strong = gate.filter_chunks(results)

    assert gate.should_refuse(strong) is True
    assert gate.refusal_response() == "Not found in documents"


def test_accept_when_confident():
    gate = ConfidenceGate()

    results = [
        {"chunk_id": "c1", "score": 0.9, "text": "strong evidence"},
        {"chunk_id": "c2", "score": 0.6, "text": "supporting evidence"},
    ]

    strong = gate.filter_chunks(results)

    assert gate.should_refuse(strong) is False
