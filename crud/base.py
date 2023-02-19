from typing import Optional

from sqlalchemy.orm import Session, joinedload

from db.base import Base
from execptions import ObjectNotFound


def get_object_or_404(
    session: Session,
    model: Base,
    pk: int,
    joined_load: Optional[tuple] = None
):
    query = session.query(model).filter(model.id == pk)
    if joined_load:
        query = query.options(*[joinedload(table) for table in joined_load])
    obj = query.first()
    if not obj:
        raise ObjectNotFound
    return obj
