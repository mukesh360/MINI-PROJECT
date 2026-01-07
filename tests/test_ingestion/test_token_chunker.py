import pytest
import tiktoken

# import the function you want to test
from ingestion.chunking.token_chunker import token_chunk

# -----------------------------
# FIXTURES
# -----------------------------

@pytest.fixture
def tokenizer():
    return tiktoken.get_encoding("cl100k_base")


@pytest.fixture
def sample_text():
    return (
        "This is the first paragraph.\n\n"
        "This is the second paragraph with more text.\n\n"
        "This is the third paragraph."
    )

# -----------------------------
# TESTS
# -----------------------------

def test_token_chunk_returns_list(sample_text):
    chunks = token_chunk(sample_text, max_tokens=50, overlap=10)
    assert isinstance(chunks, list)


def test_token_chunk_not_empty(sample_text):
    chunks = token_chunk(sample_text, max_tokens=50, overlap=10)
    assert len(chunks) > 0


def test_each_chunk_within_max_tokens(sample_text):
    max_tokens = 40
    chunks = token_chunk(sample_text, max_tokens=max_tokens, overlap=10)

    for chunk in chunks:
        assert len(chunk) <= max_tokens


def test_overlap_between_chunks(sample_text):
    max_tokens = 30
    overlap = 5

    chunks = token_chunk(sample_text, max_tokens, overlap)

    if len(chunks) > 1:
        first_chunk = chunks[0]
        second_chunk = chunks[1]

        assert first_chunk[-overlap:] == second_chunk[:overlap]


def test_empty_text_returns_empty_list():
    chunks = token_chunk("", max_tokens=50, overlap=10)
    assert chunks == []


def test_small_text_single_chunk():
    text = "Short text."
    chunks = token_chunk(text, max_tokens=100, overlap=10)

    assert len(chunks) == 1


def test_chunk_decoding_is_valid(sample_text, tokenizer):
    chunks = token_chunk(sample_text, max_tokens=50, overlap=10)

    for chunk in chunks:
        decoded = tokenizer.decode(chunk)
        assert isinstance(decoded, str)
        assert len(decoded.strip()) > 0
