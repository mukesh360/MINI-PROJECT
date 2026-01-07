import tempfile
from ingestion.csv.normalize import extract_text_from_csv


def test_extract_text_from_csv_simple():
    content = "name,age\nAlice,30\nBob,25\n"

    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", delete=False) as f:
        f.write(content)
        path = f.name

    records = extract_text_from_csv(path)

    assert len(records) == 2
    assert records[0]["row"] == 1
    assert "Alice" in records[0]["text"]
    assert "30" in records[0]["text"]
