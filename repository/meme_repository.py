from repository.database.db import SessionLocal
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from repository.database.db import Base

class Meme(Base):
    __tablename__ = "memes"

    meme_id = Column(Integer, primary_key=True, index=True)
    headline = Column(String)
    top_text = Column(String)
    bottom_text = Column(String)
    image_path = Column(String)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MemeRepository:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, headline, top, bottom, image):
        meme = Meme(
            headline=headline,
            top_text=top,
            bottom_text=bottom,
            image_path=image
        )
        self.db.add(meme)
        self.db.commit()
        self.db.refresh(meme)
        return meme

    def get_all(self):
        return self.db.query(Meme).order_by(Meme.meme_id.desc()).all()

    def get(self, meme_id):
        return self.db.query(Meme).filter(Meme.meme_id == meme_id).first()

    def delete(self, meme_id):
        meme = self.get(meme_id)
        if meme:
            self.db.delete(meme)
            self.db.commit()
