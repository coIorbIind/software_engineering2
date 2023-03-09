from fastapi import FastAPI
from sqlalchemy import create_engine

from logic.router import api_router
from logic.execptions import BaseAPIException, exception_handler
from db.base import Base
from logic.config import settings

Base.metadata.create_all(bind=create_engine(settings.database_url))


def get_app():
    app = FastAPI()
    app.include_router(api_router, prefix='/api/v1')
    app.exception_handler(BaseAPIException)(exception_handler)

    return app
