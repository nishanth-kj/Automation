from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
import os

class EmbeddingService:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.local_path = os.path.join("models", model_name.split("/")[-1])
        os.makedirs(self.local_path, exist_ok=True)
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, 
            cache_dir=self.local_path
        )
        self.model = AutoModel.from_pretrained(
            model_name, 
            cache_dir=self.local_path
        )

    def get_embeddings(self, texts):
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Mean pooling
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.numpy()

    def cosine_similarity(self, vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
