from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os
import tempfile

from retrieval.pipeline import RetrievalPipeline
from storage.registry import ingest_jsonl


app = FastAPI()

# Allow React connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = RetrievalPipeline()


# ---------- Request Models ----------

class QueryRequest(BaseModel):
    question: str


# ---------- LLaMA CALL ----------

def call_llama(context: str, question: str) -> str:
    prompt = f"""
You are an intelligent assistant.
Answer strictly using the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

    result = subprocess.run(
        ["ollama", "run", "llama3:latest"],
        input=prompt,
        text=True,
        capture_output=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result.stdout.strip()


# ---------- FILE UPLOAD ----------

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1].lower()

    if ext not in ["pdf", "csv"]:
        raise HTTPException(status_code=400, detail="Only PDF or CSV allowed")

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name

    """
    At this point:
    - You should already have a pipeline that converts PDF/CSV → JSONL chunks
    - That JSONL file is passed to ingest_jsonl()
    """

    jsonl_path = temp_path + ".jsonl"

    # ⬇️ YOU MUST ALREADY HAVE THIS FUNCTION
    # convert_to_jsonl(temp_path, jsonl_path)

    if not os.path.exists(jsonl_path):
        raise HTTPException(
            status_code=500,
            detail="Chunking step missing: JSONL not generated"
        )

    ingest_jsonl(jsonl_path)

    return {"status": "file indexed successfully"}


# ---------- QUERY ----------

@app.post("/query")
async def query_llm(req: QueryRequest):
    context = pipeline.get_context(req.question, max_chunks=5)

    if not context.strip():
        return {"answer": "No relevant context found"}

    answer = call_llama(context, req.question)

    return {
        "question": req.question,
        "answer": answer
    }


# ---------- HEALTH ----------

@app.get("/health")
def health():
    return {"status": "ok"}
