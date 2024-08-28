from fastapi import APIRouter

from app.routers import user, ai

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user.router)
api_router.include_router(ai.router)
