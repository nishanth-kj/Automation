from repository.database.db import SessionLocal
from sqlalchemy import Column, Integer, String, BigInteger
from repository.database.db import Base
from utils.contants.status import Status
from utils.time_utils import TimeUtils
from utils.logger import logger
from utils.pagination import Page

class Meme(Base):
    __tablename__ = "memes"

    meme_id = Column(Integer, primary_key=True, index=True)
    headline = Column(String)
    top_text = Column(String)
    bottom_text = Column(String)
    image_path = Column(String)
    status = Column(Integer, default=Status.ACTIVE.code)
    created_at = Column(BigInteger, default=TimeUtils.now_epoch)
    updated_at = Column(BigInteger, default=TimeUtils.now_epoch, onupdate=TimeUtils.now_epoch)

class MemeRepository:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, headline, top, bottom, image):
        logger.info(f"DB: Saving new meme for '{headline}'")
        meme = Meme(
            headline=headline,
            top_text=top,
            bottom_text=bottom,
            image_path=image,
            status=Status.ACTIVE.code,
            created_at=TimeUtils.now_epoch(),
            updated_at=TimeUtils.now_epoch()
        )
        self.db.add(meme)
        self.db.commit()
        self.db.refresh(meme)
        return meme

    def get_all(self, page=0, size=20, sort_by="newest", sort_order="desc"):
        query = self.db.query(Meme).filter(Meme.status == Status.ACTIVE.code)
        total_elements = query.count()
        
        col = Meme.created_at if sort_by == "newest" else Meme.meme_id
        if sort_order.lower() == "desc":
            query = query.order_by(col.desc())
        else:
            query = query.order_by(col.asc())
            
        content = query.limit(size).offset(page * size).all()
        return Page.create(content, page, size, total_elements)

    def get_by_id(self, meme_id):
        return self.db.query(Meme).filter(Meme.meme_id == meme_id).first()

    def delete(self, meme_id):
        logger.info(f"DB: Soft-deleting meme {meme_id}")
        meme = self.get_by_id(meme_id)
        if meme:
            meme.status = Status.DELETED.code
            meme.updated_at = TimeUtils.now_epoch()
            self.db.commit()
