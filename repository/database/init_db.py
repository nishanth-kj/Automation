from repository.database.db import engine, Base
from repository.meme_repository import Meme
from repository.news_repository import News
from repository.setting_repository import Setting
from repository.rag_repository import NewsEmbedding

def init_db():
    Base.metadata.create_all(bind=engine)