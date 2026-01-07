# storage/registry.py

import json
import uuid

from storage.db import get_connection


def ingest_jsonl(jsonl_path: str):
    """
    Ingest preprocessed JSONL chunks into DuckDB.

    - Batch inserts chunks
    - Transaction safe
    - Updates files.num_chunks
    """

    chunks = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))

    if not chunks:
        return

    file_id = chunks[0]["source_file"]
    num_chunks = len(chunks)

    conn = get_connection()

    try:
        conn.execute("BEGIN")

        # Upsert file record
        conn.execute(
            """
            INSERT INTO files (file_id, source_path, num_chunks)
            VALUES (?, ?, ?)
            ON CONFLICT (file_id)
            DO UPDATE SET num_chunks = excluded.num_chunks
            """,
            (file_id, jsonl_path, num_chunks)
        )

        # Insert chunks
        rows = []
        for idx, chunk in enumerate(chunks):
            rows.append((
                str(uuid.uuid4()),
                file_id,
                idx,
                chunk["text"],
                json.dumps({
                    "source_type": chunk.get("source_type"),
                    "location": chunk.get("location")
                })
            ))

        conn.executemany(
            """
            INSERT INTO chunks (
                chunk_id,
                file_id,
                chunk_index,
                content,
                metadata
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            rows
        )

        conn.execute("COMMIT")

    except Exception:
        conn.execute("ROLLBACK")
        raise

    finally:
        conn.close()

def load_all_chunks():
    """
    Load all chunk contents from DuckDB.
    Returns: List[str]
    """
    conn = get_connection()

    try:
        rows = conn.execute(
            "SELECT content FROM chunks ORDER BY file_id, chunk_index"
        ).fetchall()

        return [row[0] for row in rows]

    finally:
        conn.close()
