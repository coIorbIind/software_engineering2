import sys
from sqlalchemy.orm import joinedload

from db import Tag
from db.base import get_session
from execptions import ObjectNotFound, ConsoleError


def get_tag_from_console():
    if len(sys.argv) < 2:
        raise ConsoleError('Не передан id тега')
    try:
        ind = int(sys.argv[1])
        if ind <= 0:
            raise ValueError
    except ValueError:
        raise ConsoleError('Id тега должен быть целым положительным числом числом')

    session = next(get_session())

    tag = session.query(Tag).filter(Tag.id == ind).options(joinedload('articles')).first()
    if tag is None:
        raise ObjectNotFound

    print(len(tag.articles))
