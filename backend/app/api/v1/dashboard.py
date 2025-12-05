from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.dashboard import DashboardStats, RecentPrayersResponse
from app.schemas.prayer import PrayerWithProgress, PrayerResponse
from app.services.stats_service import StatsService
from app.services.prayer_service import PrayerService
from app.services.progress_service import ProgressService


router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """대시보드 통계"""
    stats = await StatsService.get_dashboard_stats(db, current_user.id)
    return DashboardStats(**stats)


@router.get("/recent", response_model=RecentPrayersResponse)
async def get_recent_prayers(
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """최근 기도 목록"""
    prayers = await StatsService.get_recent_prayers(db, current_user.id, limit)
    
    # 각 기도에 progress_count와 prayer_days 추가
    prayers_with_progress = []
    for prayer in prayers:
        progress_count = await ProgressService.get_progress_count(db, prayer.id)
        prayer_days = PrayerService.calculate_prayer_days(prayer)
        
        prayer_dict = PrayerResponse.model_validate(prayer).model_dump()
        prayer_dict["progress_count"] = progress_count
        prayer_dict["prayer_days"] = prayer_days
        
        prayers_with_progress.append(PrayerWithProgress(**prayer_dict))
    
    return RecentPrayersResponse(
        items=prayers_with_progress,
        total=len(prayers_with_progress)
    )
