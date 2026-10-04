import faiss
import numpy as np


class BugVectorStore:
    """
    FAISS-based vector store for bug embeddings.
    """

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)

    def add(self, embeddings):
        vectors = embeddings.cpu().numpy().astype(np.float32)
        self.index.add(vectors)

    def search(self, query_embedding, top_k: int = 5):
        query_vector = query_embedding.cpu().numpy().astype(np.float32)

        scores, indices = self.index.search(
            query_vector.reshape(1, -1),
            top_k,
        )

        return scores[0], indices[0]

    @property
    def size(self) -> int:
        return self.index.ntotal