CREATE TABLE IF NOT EXISTS files (
    file_id TEXT PRIMARY KEY,
    source_path TEXT NOT NULL,
    num_chunks INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS chunks (
    chunk_id TEXT PRIMARY KEY,
    file_id TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    metadata JSON,
    FOREIGN KEY (file_id) REFERENCES files(file_id)
);
