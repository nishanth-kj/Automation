from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from repository.database.db import Base, SessionLocal

class News(Base):
    __tablename__ = "news"

    news_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    url = Column(String)
    source = Column(String)
    image_url = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    category = Column(String, default="trending")
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class NewsRepository:
    def __init__(self):
        self.db = SessionLocal()

    def save_all(self, news_items):
        for item in news_items:
            # Check if title already exists to avoid duplicates
            exists = self.db.query(News).filter(News.title == item["title"]).first()
            if not exists:
                news = News(
                    title=item["title"],
                    url=item["url"],
                    source=item["source"],
                    image_url=item.get("image_url"),
                    category=item.get("category", "trending")
                )
                self.db.add(news)
        self.db.commit()

    def get_news(self, limit=20, offset=0, sort_by="newest"):
        query = self.db.query(News)
        
        if sort_by == "newest":
            query = query.order_by(News.created_at.desc())
        elif sort_by == "source":
            query = query.order_by(News.source)
            
        return query.limit(limit).offset(offset).all()
