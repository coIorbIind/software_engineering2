from typing import Iterator, Optional
from functools import lru_cache

from sqlalchemy.orm import Session, declarative_base

from fastapi_utils.session import FastAPISessionMaker

from logic.config import settings


def get_session(url: Optional[str] = None) -> Iterator[Session]:
    yield from fastapi_session_maker(url).get_db()


def get_session_for_api() -> Iterator[Session]:
    yield from fastapi_session_maker().get_db()


@lru_cache()
def fastapi_session_maker(url: Optional[str] = None) -> FastAPISessionMaker:
    if not url:
        url = settings.database_url
    return FastAPISessionMaker(url)


Base = declarative_base()
