import numpy as np
from services.embedding_service import EmbeddingService
from repository.news_repository import NewsRepository
from repository.rag_repository import RagRepository

class RagService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.news_repo = NewsRepository()
        self.rag_repo = RagRepository()

    def build_index(self):
        # Fetch all active news
        news_page = self.news_repo.get_all(size=1000)
        news_items = news_page.content
        
        if not news_items: return 0
        
        # Clear existing
        self.rag_repo.clear()
        
        count = 0
        for item in news_items:
            text = f"{item.title} {item.content or ''}"
            vec = self.embedding_service.get_embeddings([text])[0]
            self.rag_repo.save_embedding(item.news_id, vec)
            count += 1
            
        return count

    def search(self, query, top_k=3):
        # Load all from DB for searching
        all_embs = self.rag_repo.get_all()
        if not all_embs: return []
        
        query_vec = self.embedding_service.get_embeddings([query])[0]
        
        results = []
        for row in all_embs:
            # Convert bytes back to numpy array
            # We need the original shape/dtype. all-MiniLM-L6-v2 is float32, size 384.
            vec = np.frombuffer(row.embedding, dtype=np.float32)
            sim = self.embedding_service.cosine_similarity(query_vec, vec)
            
            # Fetch news meta from DB
            news = self.news_repo.get_by_id(row.news_id)
            if news:
                results.append((sim, {
                    "news_id": news.news_id,
                    "title": news.title,
                    "source": news.source
                }))
            
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_k]
