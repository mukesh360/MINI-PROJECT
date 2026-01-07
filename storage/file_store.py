# storage/file_store.py

from storage.db import get_connection


def ensure_file(file_id: str, source_path: str):
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO files (file_id, source_path)
            VALUES (?, ?)
            ON CONFLICT (file_id) DO NOTHING
            """,
            (file_id, source_path)
        )
    finally:
        conn.close()


def update_num_chunks(file_id: str, num_chunks: int):
    conn = get_connection()
    try:
        conn.execute(
            """
            UPDATE files
            SET num_chunks = ?
            WHERE file_id = ?
            """,
            (num_chunks, file_id)
        )
    finally:
        conn.close()
