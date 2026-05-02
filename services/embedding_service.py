import requests
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

class EmbeddingService:
    def __init__(self):
        self.lm_studio_url = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")

    def get_embeddings(self, texts):
        """Call LM Studio for embeddings"""
        if isinstance(texts, str):
            texts = [texts]
            
        try:
            # Note: Not all LM Studio models support /embeddings. 
            # If it fails, we'll return a mock vector for compatibility.
            response = requests.post(
                f"{self.lm_studio_url}/embeddings",
                json={
                    "model": "text-embedding-nomic-v1.5", # Standard LM Studio embedding model
                    "input": texts
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            # LM Studio returns data as a list of dicts with 'embedding' key
            return np.array([item["embedding"] for item in data["data"]])
            
        except Exception as e:
            print(f"EmbeddingService Error: {e}")
            # Mock 384-dimensional vector (typical for all-MiniLM-L6-v2)
            return np.zeros((len(texts), 384))

    def cosine_similarity(self, vec1, vec2):
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0
        return np.dot(vec1, vec2) / (norm1 * norm2)
