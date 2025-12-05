from fastapi import APIRouter
from app.api.v1 import auth, prayers, progress, dashboard

api_router = APIRouter()

# 라우터 등록
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(prayers.router, prefix="/prayers", tags=["prayers"])
api_router.include_router(progress.router, prefix="/prayers", tags=["progress"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
