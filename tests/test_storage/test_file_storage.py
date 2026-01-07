# tests/test_storage/test_file_store.py

from storage import db
from storage.file_store import ensure_file, update_num_chunks


def test_ensure_file_and_update(tmp_path, monkeypatch):
    temp_db = tmp_path / "test.duckdb"
    monkeypatch.setattr(db, "DB_PATH", str(temp_db))

    file_id = "file_123"
    path = "/tmp/source.pdf"

    ensure_file(file_id, path)
    update_num_chunks(file_id, 5)

    conn = db.get_connection()
    row = conn.execute(
        "SELECT file_id, source_path, num_chunks FROM files"
    ).fetchone()

    assert row == (file_id, path, 5)

    conn.close()
