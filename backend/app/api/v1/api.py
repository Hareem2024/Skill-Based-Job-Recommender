"""
Main API router that includes all endpoint routers.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, resumes, jobs, analytics, recommendations, chat

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

