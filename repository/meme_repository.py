from repository.database.db import SessionLocal
from sqlalchemy import Column, Integer, String, BigInteger
from repository.database.db import Base
from utils.contants.status import Status
from utils.time_utils import TimeUtils

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

    def get_all(self):
        return self.db.query(Meme).filter(Meme.status == Status.ACTIVE.code).order_by(Meme.meme_id.desc()).all()

    def get(self, meme_id):
        return self.db.query(Meme).filter(Meme.meme_id == meme_id).first()

    def delete(self, meme_id):
        meme = self.get(meme_id)
        if meme:
            meme.status = Status.INACTIVE.code
            meme.updated_at = TimeUtils.now_epoch()
            self.db.commit()
