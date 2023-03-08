import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, session

from db.base import Base, get_session
from main import get_app

from .fixtures.article import article_factory


@pytest.fixture
def scope_session() -> Session:
    db_session = next(get_session())
    Base.metadata.bind = db_session.bind
    session.close_all_sessions()
    Base.metadata.drop_all()
    Base.metadata.create_all()
    return db_session


@pytest.fixture
def client() -> TestClient:
    yield TestClient(get_app())
