import json
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

def token_chunk(text, max_tokens, overlap):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    token_buffer = []

    for para in paragraphs:
        tokens = enc.encode(para)

        for tok in tokens:
            token_buffer.append(tok)

            if len(token_buffer) == max_tokens:
                chunks.append(token_buffer[:])
                token_buffer = token_buffer[max_tokens - overlap:]

    if token_buffer:
        chunks.append(token_buffer)

    return chunks


# 👇 SCRIPT ENTRY POINT (IMPORTANT)
if __name__ == "__main__":
    INPUT_FILE = "input.jsonl"
    OUTPUT_FILE = "chunks.txt"
    MAX_TOKENS = 400
    OVERLAP = 60

    chunk_id = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as fin, \
         open(OUTPUT_FILE, "w", encoding="utf-8") as fout:

        for row_id, line in enumerate(fin):
            record = json.loads(line)

            text = record["text"]
            file_id = record.get("file_id", "unknown")
            page = record.get("page", row_id)

            token_chunks = token_chunk(text, MAX_TOKENS, OVERLAP)

            for tokens in token_chunks:
                if not tokens:
                    continue

                chunk_text = enc.decode(tokens)

                fout.write(
                    f"CHUNK_ID: {chunk_id}\n"
                    f"FILE_ID: {file_id}\n"
                    f"PAGE: {page}\n"
                    f"TOKENS: {len(tokens)}\n"
                    f"TEXT:\n{chunk_text}\n"
                    f"{'-'*60}\n"
                )

                chunk_id += 1

    print("✅ Token-based chunking completed successfully")
