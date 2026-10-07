from fastapi import APIRouter

from app.api.routes.health_router import router as health_router
from app.api.routes.payload_router import router as payload_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(payload_router)

__all__ = ['api_router']
