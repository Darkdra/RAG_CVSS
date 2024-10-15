from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings


class CustomEmbeddings(Embeddings):
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        return [self.model.encode(d).tolist() for d in documents]

    def embed_query(self, query: str) -> list[float]:
        return self.model.encode([query])[0].tolist()
