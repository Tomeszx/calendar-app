import os

from models.db_event import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__))) + "/app.db"
DATABASE_URL = f"sqlite:///{FILE_PATH}"


engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()
