from fastapi import APIRouter

from .webhook import router

webhook_router = APIRouter()
webhook_router.include_router(router, tags=["Webhook模块"])

__all__ = ["webhook_router"]
