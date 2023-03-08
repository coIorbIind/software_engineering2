from fastapi import FastAPI
from sqlalchemy import create_engine

from router import api_router
from execptions import BaseAPIException, exception_handler
from db.base import Base
from config import settings

Base.metadata.create_all(bind=create_engine(settings.database_url))


def get_app():
    app = FastAPI()
    app.include_router(api_router, prefix='/api/v1')
    app.exception_handler(BaseAPIException)(exception_handler)

    return app
