from typing import Iterator
from functools import lru_cache

from sqlalchemy.orm import Session, declarative_base

from fastapi_utils.session import FastAPISessionMaker

from config import settings


def get_session() -> Iterator[Session]:
    yield from fastapi_session_maker().get_db()


@lru_cache()
def fastapi_session_maker() -> FastAPISessionMaker:
    return FastAPISessionMaker(settings.database_url)


Base = declarative_base()
