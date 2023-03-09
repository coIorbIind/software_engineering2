import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, session

from db.base import Base, get_session
from logic.config import settings
from main import get_app

from .fixtures.article import article_factory, article_tag_factory
from .fixtures.tag import tag_factory


@pytest.fixture
def scope_session() -> Session:
    session.close_all_sessions()
    engine = create_engine(settings.database_url)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return next(get_session())


@pytest.fixture
def client() -> TestClient:
    yield TestClient(get_app())
