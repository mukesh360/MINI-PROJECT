import os
import magic

import json
import os
import tiktoken

from ingestion.pdf.extract import extract_text_from_pdf
from ingestion.csv.normalize import extract_text_from_csv
from ingestion.chunking.token_chunker import TokenChunker


# Stable tokenizer (same as OpenAI / LLaMA family)
enc = tiktoken.get_encoding("cl100k_base")


def convert_to_jsonl(input_path: str, output_path: str):
    """
    Convert PDF or CSV to token-based JSONL chunks.
    """

    records = []

    # -------------------------------------------------
    # LOAD RAW TEXT
    # -------------------------------------------------
    if input_path.lower().endswith(".pdf"):
        pages = extract_text_from_pdf(input_path)

        for page_num, text in enumerate(pages):
            if not isinstance(text, str) or not text.strip():
                continue

            records.append({
                "text": text,
                "page": page_num
            })

    elif input_path.lower().endswith(".csv"):
        csv_rows = extract_text_from_csv(input_path)

        for row in csv_rows:
            # row is a dict → extract text field
            text = row.get("text")

            if not isinstance(text, str) or not text.strip():
                continue

            records.append({
                "text": text,
                "row": row.get("row")
            })

    else:
        raise ValueError("Unsupported file type")

    # -------------------------------------------------
    # PREPARE OUTPUT DIRECTORY
    # -------------------------------------------------
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # -------------------------------------------------
    # CHUNK + WRITE JSONL
    # -------------------------------------------------
    chunk_id = 0

    with open(output_path, "w", encoding="utf-8") as fout:
        for record in records:
            text = record["text"]

            token_chunks = token_chunk(
                text=text,
                max_tokens=400,
                overlap=60
            )

            for tokens in token_chunks:
                if not tokens:
                    continue

                fout.write(json.dumps({
                    "chunk_id": f"chunk_{chunk_id}",
                    "text": enc.decode(tokens),
                    "page": record.get("page"),
                    "row": record.get("row"),
                }) + "\n")

                chunk_id += 1


def detect_file_type(file_path: str) -> str:
    """
    Detect file type using MIME sniffing instead of extension.
    """
    if not os.path.exists(file_path):
        return "unsupported"

    mime = magic.from_file(file_path, mime=True)

    if mime == "application/pdf":
        return "pdf"
    elif mime in ("text/csv", "application/csv", "application/vnd.ms-excel"):
        return "csv"
    elif mime.startswith("text/"):
        return "txt"
    else:
        return "unsupported"


'''
import os

def detect_file_type(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return "pdf"
    elif ext == ".csv":
        return "csv"
    elif ext == ".txt":
        return "txt"
    else:
        return "unsupported"

'''