from sentence_transformers import SentenceTransformer
import torch
from torch import F


class MiniLM:
    def __init__(self, model="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model)

    def sort_by_centroid(self, sentences: list[str]) -> list[str]:
        embeddings = torch.tensor(self.model.encode(sentences))
        normalized_vectors = F.normalize(embeddings, p=2, dim=1)
        centroid = normalized_vectors.mean(dim=0, keepdim=True)
        similarities = torch.matmul(normalized_vectors, centroid.T).flatten()
        sorted_indices = torch.argsort(similarities, descending=True)
        return [sentences[i] for i in sorted_indices]