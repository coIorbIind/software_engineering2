from fastapi import APIRouter

from api.routes.article import router as posts_router

api_router = APIRouter()
api_router.include_router(posts_router, prefix='/posts', tags=['posts'])
