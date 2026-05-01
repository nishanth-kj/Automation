from sqlalchemy import Column, Integer, String, Text, BigInteger
from repository.database.db import Base, SessionLocal
from utils.contants.status import Status
from utils.time_utils import TimeUtils

class News(Base):
    __tablename__ = "news"

    news_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    url = Column(String)
    source = Column(String)
    image_url = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    category = Column(String, default="trending")
    status = Column(Integer, default=Status.ACTIVE.code)
    created_at = Column(BigInteger, default=TimeUtils.now_epoch)
    updated_at = Column(BigInteger, default=TimeUtils.now_epoch, onupdate=TimeUtils.now_epoch)

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
                    category=item.get("category", "trending"),
                    status=Status.ACTIVE.code,
                    created_at=TimeUtils.now_epoch(),
                    updated_at=TimeUtils.now_epoch()
                )
                self.db.add(news)
        self.db.commit()

    def get_news(self, limit=20, offset=0, sort_by="newest"):
        query = self.db.query(News).filter(News.status == Status.ACTIVE.code)
        
        if sort_by == "newest":
            query = query.order_by(News.created_at.desc())
        elif sort_by == "source":
            query = query.order_by(News.source)
            
        return query.limit(limit).offset(offset).all()
