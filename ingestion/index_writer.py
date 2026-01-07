# ingestion/index_writer.py

from typing import List, Dict
import faiss
import numpy as np
import os
import json

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

        # Cosine similarity via inner product (normalized vectors)
        self.index = faiss.IndexFlatIP(self.dim)

        self.id_map: Dict[int, str] = {}

    def build_index(
        self,
        chunk_ids: List[str],
        texts: List[str],
    ):
        assert len(chunk_ids) == len(texts), "Chunk IDs and texts mismatch"

        embeddings = self.embedder.embed_texts(texts)

        # Add vectors to FAISS
        self.index.add(embeddings)

        # Build ID map
        start_id = len(self.id_map)
        for i, chunk_id in enumerate(chunk_ids):
            self.id_map[start_id + i] = chunk_id

        self._validate(len(chunk_ids))

    def save(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)

        faiss.write_index(self.index, self.index_path)

        with open(self.mapping_path, "w", encoding="utf-8") as f:
            json.dump(self.id_map, f, indent=2)

    def _validate(self, expected_count: int):
        assert (
            self.index.ntotal == expected_count
        ), f"FAISS size {self.index.ntotal} != chunk count {expected_count}"
