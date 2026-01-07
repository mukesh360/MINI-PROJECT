# storage/db.py

import duckdb
from pathlib import Path

DB_PATH = "storage.duckdb"


def get_connection():
    conn = duckdb.connect(DB_PATH)

    schema_path = Path(__file__).parent / "schema.sql"
    if schema_path.exists():
        conn.execute(schema_path.read_text())

    return conn
