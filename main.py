from fastapi import FastAPI

from router import api_router
from execptions import BaseAPIException, exception_handler


app = FastAPI()


@app.get("/ping")
async def ping():
    return {'result': 'pong'}


app.include_router(api_router, prefix='/api/v1')


app.exception_handler(BaseAPIException)(exception_handler)
