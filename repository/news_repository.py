from sqlalchemy import Column, Integer, String, Text, BigInteger
from repository.database.db import Base, SessionLocal
from utils.contants.status import Status
from utils.time_utils import TimeUtils
from utils.logger import logger
from utils.pagination import Page

class News(Base):
    __tablename__ = "news"

    news_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    url = Column(String)
    source = Column(String)
    image_url = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    category = Column(String, default="trending")
    status = Column(Integer, default=Status.PENDING.code)
    created_at = Column(BigInteger, default=TimeUtils.now_epoch)
    updated_at = Column(BigInteger, default=TimeUtils.now_epoch, onupdate=TimeUtils.now_epoch)

class NewsRepository:
    def __init__(self):
        self.db = SessionLocal()

    def save_all(self, news_items, status=Status.PENDING.code):
        saved_ids = []
        for item in news_items:
            try:
                exists = self.db.query(News).filter(News.title == item["title"]).first()
                if not exists:
                    news = News(
                        title=item["title"],
                        url=item["url"],
                        source=item["source"],
                        image_url=item.get("image_url"),
                        category=item.get("category", "trending"),
                        status=status,
                        created_at=TimeUtils.now_epoch(),
                        updated_at=TimeUtils.now_epoch()
                    )
                    self.db.add(news)
                    self.db.flush()
                    saved_ids.append(news.news_id)
            except Exception as e:
                logger.error(f"Failed to save news item '{item.get('title')}': {e}")
                self.db.rollback()
        self.db.commit()
        return saved_ids

    def update_status(self, news_ids, new_status):
        logger.info(f"DB: Updating status for {len(news_ids)} news items to code {new_status}")
        self.db.query(News).filter(News.news_id.in_(news_ids)).update(
            {News.status: new_status, News.updated_at: TimeUtils.now_epoch()},
            synchronize_session=False
        )
        self.db.commit()

    def delete(self, news_id):
        logger.info(f"DB: Soft-deleting news item {news_id}")
        news = self.get_by_id(news_id)
        if news:
            news.status = Status.DELETED.code
            news.updated_at = TimeUtils.now_epoch()
            self.db.commit()

    def get_by_id(self, news_id):
        obj = self.db.query(News).filter(News.news_id == news_id).first()
        if not obj:
            return None
        return {
            "news_id": obj.news_id,
            "title": obj.title,
            "url": obj.url,
            "source": obj.source,
            "image_url": obj.image_url,
            "content": obj.content,
            "category": obj.category,
            "status": obj.status,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at
        }

    def get_all(self, page=0, size=20, sort_by="newest", sort_order="desc"):
        logger.info(f"DB: Fetching news page {page} with size {size}")
        query = self.db.query(News).filter(News.status == Status.ACTIVE.code)
        total_elements = query.count()
        
        if sort_by == "newest":
            col = News.created_at
        elif sort_by == "source":
            col = News.source
        else:
            col = News.news_id

        if sort_order.lower() == "desc":
            query = query.order_by(col.desc())
        else:
            query = query.order_by(col.asc())
            
        content_objs = query.limit(size).offset(page * size).all()
        
        # Convert to dicts for Pydantic serialization
        content = []
        for obj in content_objs:
            content.append({
                "news_id": obj.news_id,
                "title": obj.title,
                "url": obj.url,
                "source": obj.source,
                "image_url": obj.image_url,
                "content": obj.content,
                "category": obj.category,
                "status": obj.status,
                "created_at": obj.created_at,
                "updated_at": obj.updated_at
            })
            
        return Page.create(content, page, size, total_elements)
