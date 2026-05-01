from repository.database.db import engine, Base
from repository.meme_repository import Meme

from repository.news_repository import News

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()