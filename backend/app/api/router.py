from fastapi import APIRouter
from app.api.v1 import health, analysis, history, chat, auth

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(health.router, tags=["health"])
api_router.include_router(analysis.router, tags=["analysis"])
api_router.include_router(history.router, tags=["history"])
api_router.include_router(chat.router, tags=["chat"])
