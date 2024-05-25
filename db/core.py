from model.db_event import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///db/test.db"


class NotFoundError(Exception):
    pass


engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()
