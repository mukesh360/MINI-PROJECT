# tests/test_storage/test_registry.py

import json
from storage import db
from storage.registry import ingest_jsonl


def test_ingest_jsonl(tmp_path, monkeypatch):
    temp_db = tmp_path / "test.duckdb"
    monkeypatch.setattr(db, "DB_PATH", str(temp_db))

    jsonl_path = tmp_path / "chunks.jsonl"

    chunks = [
        {
            "source_file": "doc1.pdf",
            "text": "First chunk text",
            "source_type": "pdf",
            "location": {"page": 1}
        },
        {
            "source_file": "doc1.pdf",
            "text": "Second chunk text",
            "source_type": "pdf",
            "location": {"page": 2}
        }
    ]

    with open(jsonl_path, "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c) + "\n")

    ingest_jsonl(str(jsonl_path))

    conn = db.get_connection()

    files = conn.execute(
        "SELECT file_id, num_chunks FROM files"
    ).fetchall()

    chunks_db = conn.execute(
        "SELECT content FROM chunks ORDER BY chunk_index"
    ).fetchall()

    assert files == [("doc1.pdf", 2)]
    assert [c[0] for c in chunks_db] == [
        "First chunk text",
        "Second chunk text",
    ]

    conn.close()
