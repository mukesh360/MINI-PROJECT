from pathlib import Path
import json
from typing import Union, List

from ingestion.pdf.extract import extract_text_from_pdf
from ingestion.csv.normalize import extract_text_from_csv
from ingestion.chunking.chunker import chunk_text
from storage.registry import ingest_jsonl


def ingest_file(file_path: str):
    """
    Ingest a single file (PDF / CSV / TXT) into DuckDB.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(file_path)

    # -------------------------
    # 1. Extract raw text
    # -------------------------
    if path.suffix.lower() == ".pdf":
        text: Union[str, List[str]] = extract_text_from_pdf(str(path))

    elif path.suffix.lower() == ".csv":
        text = extract_text_from_csv(str(path))

    elif path.suffix.lower() in {".txt", ".md"}:
        text = path.read_text(encoding="utf-8")

    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    # -------------------------
    # 2. Normalize to string
    # -------------------------
    if isinstance(text, list):
        normalized_lines = []

        for row in text:
            if isinstance(row, dict):
                line = " | ".join(
                    f"{k}: {v}" for k, v in row.items() if v is not None
                )
                if line.strip():
                    normalized_lines.append(line)

            elif isinstance(row, str):
                if row.strip():
                    normalized_lines.append(row)

        text = "\n".join(normalized_lines)

    if not text.strip():
        print(f"⚠️ Skipping empty file: {path}")
        return


    # -------------------------
    # 3. Chunk text
    # -------------------------
    chunks = chunk_text(text)

    if not chunks:
        print(f"⚠️ No chunks produced: {path}")
        return

    # -------------------------
    # 4. Write JSONL
    # -------------------------
    jsonl_path = path.with_suffix(".jsonl")

    with open(jsonl_path, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            record = {
                "source_file": str(path),
                "chunk_index": i,
                "text": chunk,
                "source_type": path.suffix.lstrip("."),
                "location": None,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # -------------------------
    # 5. Insert into DB
    # -------------------------
    ingest_jsonl(str(jsonl_path))

    print(f"✅ Ingested {len(chunks)} chunks from {path}")
