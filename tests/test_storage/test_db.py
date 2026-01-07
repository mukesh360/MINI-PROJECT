# tests/test_storage/test_db.py

import duckdb
from pathlib import Path
from storage import db


def test_get_connection_creates_schema(tmp_path, monkeypatch):
    temp_db = tmp_path / "test.duckdb"

    monkeypatch.setattr(db, "DB_PATH", str(temp_db))

    conn = db.get_connection()

    # Verify tables exist
    tables = conn.execute(
        "SELECT table_name FROM information_schema.tables"
    ).fetchall()

    table_names = {t[0] for t in tables}

    assert "files" in table_names
    assert "chunks" in table_names

    conn.close()
