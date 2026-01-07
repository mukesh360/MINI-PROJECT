import json
import uuid
import duckdb

from storage.db import get_connection
from storage.schema import init_db


def ingest_jsonl(jsonl_path: str):
    """
    Ingest preprocessed JSONL chunks into DuckDB.

    - Batch inserts chunks
    - Uses transaction safety
    - Updates files.num_chunks
    """

    # Ensure tables exist
    init_db()

    # Read JSONL
    chunks = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))

    if not chunks:
        return

    # Derive file_id from source_file (your JSONL structure)
    file_id = chunks[0]["source_file"]
    num_chunks = len(chunks)

    conn = get_connection()

    try:
        conn.execute("BEGIN TRANSACTION")

        # Insert / upsert file record
        conn.execute(
            """
            INSERT INTO files (file_id, source_path, num_chunks)
            VALUES (?, ?, ?)
            ON CONFLICT (file_id)
            DO UPDATE SET num_chunks = excluded.num_chunks
            """,
            (file_id, jsonl_path, num_chunks)
        )

        # Prepare batch chunk insert
        chunk_rows = []
        for idx, chunk in enumerate(chunks):
            chunk_rows.append((
                str(uuid.uuid4()),     # chunk_id
                file_id,               # file_id (FK)
                idx,                   # chunk_index
                chunk["text"],         # content
                json.dumps({           # metadata
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
            chunk_rows
        )

        conn.execute("COMMIT")

    except Exception as e:
        conn.execute("ROLLBACK")
        raise e

    finally:
        conn.close()
