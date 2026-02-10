from pathlib import Path
from typing import List

from src.ingestion.chunking import chunk_text
from src.embeddings.embedder import Embedder
from src.retrieval.faiss_store import FaissStore
from src.llm.local_llm import LocalLLM


class RAGPipeline:
    def __init__(self, model_path: Path):
        self.embedder = Embedder()
        self.llm = LocalLLM(model_path=model_path)
        self.store = None

    def ingest(self, documents: List[str]):
        chunks = []
        for doc in documents:
            chunks.extend(chunk_text(doc))

        embeddings = self.embedder.embed(chunks)
        self.store = FaissStore(embedding_dim=embeddings.shape[1])
        self.store.add(embeddings, chunks)

    def query(self, question: str, top_k: int = 3) -> str:
        if self.store is None:
            raise ValueError("No documents ingested. Call ingest() first.")
        
        query_embedding = self.embedder.embed([question])
        retrieved_chunks = self.store.search(query_embedding, k=top_k)

        context = "\n\n".join(retrieved_chunks)

        prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""
        return self.llm.generate(prompt)
    
    