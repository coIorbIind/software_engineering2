from fastapi import FastAPI

from router import api_router


app = FastAPI()


@app.get("/ping")
async def ping():
    return {'result': 'pong'}


app.include_router(api_router, prefix='/api/v1')
