import os
import json
import faiss
import numpy as np
from typing import List

from ingestion.embedding import Embedder


class FaissIndexWriter:
    def __init__(
        self,
        index_path: str,
        mapping_path: str,
        model_name: str = "BAAI/bge-small-en-v1.5",
    ):
        self.index_path = index_path
        self.mapping_path = mapping_path

        self.embedder = Embedder(model_name=model_name)
        self.dim = self.embedder.dim

    def build_and_save(
        self,
        chunk_ids: List[str],
        texts: List[str],
        chunk_indices: List[int] | None = None,
    ):
        assert len(chunk_ids) == len(texts), "IDs and texts length mismatch"

        if chunk_indices is None:
            chunk_indices = list(range(len(chunk_ids)))

        # ---- Embed ----
        embeddings = self.embedder.embed_texts(texts).astype("float32")
        faiss.normalize_L2(embeddings)

        # ---- Build FAISS ----
        index = faiss.IndexFlatIP(self.dim)
        index.add(embeddings)

        index_dir = os.path.dirname(self.index_path)
        if index_dir:
            os.makedirs(index_dir, exist_ok=True)

        faiss.write_index(index, self.index_path)

        # ---- ID Mapping ----
        id_map = {
            str(i): {
                "chunk_id": chunk_ids[i],
                "chunk_index": int(chunk_indices[i]),
            }
            for i in range(len(chunk_ids))
        }

        map_dir = os.path.dirname(self.mapping_path)
        if map_dir:
            os.makedirs(map_dir, exist_ok=True)

        with open(self.mapping_path, "w", encoding="utf-8") as f:
            json.dump(id_map, f, indent=2)

        print(f"✅ FAISS index saved: {self.index_path}")
        print(f"✅ ID map saved: {self.mapping_path}")
