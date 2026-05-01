from repository.database.db import engine
from repository.meme import Meme

def init_db():
    Meme.metadata.create_all(bind=engine)