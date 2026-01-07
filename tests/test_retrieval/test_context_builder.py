from retrieval.context_builder import ContextBuilder


def test_context_token_budget():
    builder = ContextBuilder(max_tokens=20)

    chunks = [
        {"text": "This is a short sentence."},
        {"text": "This sentence is much longer and will exceed the token limit."},
    ]

    context = builder.build(chunks)

    assert context
    assert "short sentence" in context
