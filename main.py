from fastapi import FastAPI
from sqlalchemy import create_engine
import uvicorn

from logic.router import api_router
from logic.execptions import BaseAPIException, exception_handler
from db.base import Base
from logic.config import settings


def get_app():
    app = FastAPI()
    app.include_router(api_router, prefix='/api/v1')
    app.exception_handler(BaseAPIException)(exception_handler)

    @app.on_event('startup')
    async def create_db():
        Base.metadata.create_all(bind=create_engine(settings.database_url))

    return app


if __name__ == '__main__':
    uvicorn.run(get_app(), host="0.0.0.0", port=8000)
