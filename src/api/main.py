from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from pathlib import Path

from src.pipeline import RAGPipeline

# app setup
app = FastAPI(title="Smart RAG API")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "phi-2.gguf"

pipeline = RAGPipeline(model_path=MODEL_PATH)


# model call
class IngestRequest(BaseModel):
    documents: List[str]


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3


# Endpoints
@app.post("/ingest")
def ingest_docs(request: IngestRequest):
    pipeline.ingest(request.documents)
    return {"status": "documents ingested"}


@app.post("/query")
def query_docs(request: QueryRequest):
    try:
        answer = pipeline.query(request.question, top_k=request.top_k)
        return {"answer": answer}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.get("/")
def root():
    return {"status": "Smart RAG API running"}
