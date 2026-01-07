import sys
from pathlib import Path

from ingestion.data_ingestion import ingest_file
from storage.db import get_connection


def ingest_path(input_path: Path):
    """
    Ingest a file or directory into DuckDB.
    """

    if not input_path.exists():
        raise FileNotFoundError(f"Path not found: {input_path}")

    files = []

    if input_path.is_file():
        files = [input_path]

    elif input_path.is_dir():
        files = [
            p for p in input_path.rglob("*")
            if p.suffix.lower() in {".pdf", ".csv", ".txt"}
        ]

    if not files:
        print("⚠️ No ingestible files found.")
        return

    print(f"📂 Ingesting {len(files)} files...\n")

    for file_path in files:
        print(f"📥 Ingesting: {file_path}")
        ingest_file(str(file_path))

    # --- verification ---
    conn = get_connection()

    files_count = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    chunks_count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]

    print("\n✅ Ingestion complete")
    print(f"   Files indexed : {files_count}")
    print(f"   Chunks stored : {chunks_count}")

    if chunks_count == 0:
        raise RuntimeError("❌ Ingestion failed — no chunks created")


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m scripts.ingest <file_or_directory>")
        sys.exit(1)

    input_path = Path(sys.argv[1]).resolve()
    ingest_path(input_path)


if __name__ == "__main__":
    main()
