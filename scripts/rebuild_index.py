from ingestion.embedding import Embedder
from ingestion.index_writer import FaissIndexWriter
from retrieval.sparse import BM25Index
from storage.db import get_connection
import json
import os

FAISS_PATH = "vectors.faiss"
MAP_PATH = "id_map.json"
BM25_PATH = "bm25.pkl"


def main():
    conn = get_connection()

    rows = conn.execute(
        "SELECT chunk_id, content FROM chunks ORDER BY chunk_index"
    ).fetchall()

    chunk_ids = [r[0] for r in rows]
    texts = [r[1] for r in rows]

    if not texts:
        raise RuntimeError("No chunks found — ingestion not run")

    # --- Dense ---
    writer = FaissIndexWriter(
        index_path=FAISS_PATH,
        mapping_path=MAP_PATH,
    )
    writer.build_and_save(chunk_ids, texts)

    # --- Sparse ---
    bm25 = BM25Index()
    bm25.build(chunk_ids, texts)
    bm25.save(BM25_PATH)

    print("✅ Indexes built successfully")


if __name__ == "__main__":
    main()
