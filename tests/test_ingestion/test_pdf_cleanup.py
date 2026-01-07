from ingestion.pdf.cleanup import normalize_text


def test_normalize_text_basic():
    raw = "Hello   World\n\n\nThis…… is a test\u00a0"
    cleaned = normalize_text(raw)

    assert "  " not in cleaned
    assert "……" not in cleaned
    assert cleaned.count("\n") <= 2
    assert cleaned.startswith("Hello World")
