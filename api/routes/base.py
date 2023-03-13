from fastapi import Depends

from sqlalchemy.orm import Session

from db.base import get_session_for_api


class BaseRoute:
    session: Session = Depends(get_session_for_api)
    model = None
    paginator = None
