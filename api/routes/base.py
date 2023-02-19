from fastapi import Depends

from sqlalchemy.orm import Session

from db.base import get_session


class BaseRoute:
    session: Session = Depends(get_session)
    model = None
