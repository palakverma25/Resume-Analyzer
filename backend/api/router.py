from fastapi import APIRouter

from backend.api.routes.health import router as health_router
from backend.api.routes.resume import router as resume_router
from backend.api.routes.score import router as score_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(resume_router, prefix="/resume", tags=["resume"])
api_router.include_router(score_router, prefix="/resume", tags=["scoring"])
