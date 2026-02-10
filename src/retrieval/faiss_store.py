import faiss
import numpy as np
from typing import List


class FaissStore:
    def __init__(self, embedding_dim: int):
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.texts: List[str] = []

    def add(self, embeddings: np.ndarray, texts: List[str]):
        self.index.add(embeddings)
        self.texts.extend(texts)

    def search(self, query_embedding: np.ndarray, k: int = 3) -> List[str]:
        distances, indices = self.index.search(query_embedding, k)
        return [self.texts[i] for i in indices[0]]
