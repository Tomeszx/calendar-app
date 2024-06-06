import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from models.db_event import Base, DBEvent
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from tests.db_test_data import get_test_data
from db.core import get_db


client = TestClient(app)

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    database = testing_session_local()
    try:
        yield database
    finally:
        database.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_database():
    db = next(override_get_db())
    db.query(DBEvent).delete()
    for event in get_test_data():
        db.add(event)
    db.commit()
