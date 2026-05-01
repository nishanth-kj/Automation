from repository.database.db import engine, Base
from repository.meme_repository import Meme
from repository.news_repository import News
from repository.setting_repository import Setting

def init_db():
    Base.metadata.create_all(bind=engine)