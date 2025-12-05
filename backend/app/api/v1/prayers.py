from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.prayer import PrayerStatus
from app.schemas.prayer import (
    PrayerCreate,
    PrayerUpdate,
    PrayerAnswer,
    PrayerResponse,
    PrayerWithProgress,
    PrayerListResponse
)
from app.services.prayer_service import PrayerService
from app.services.progress_service import ProgressService
import math


router = APIRouter()


@router.post("/", response_model=PrayerResponse, status_code=status.HTTP_201_CREATED)
async def create_prayer(
    prayer_data: PrayerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """기도 등록"""
    prayer = await PrayerService.create_prayer(db, current_user.id, prayer_data)
    return PrayerResponse.model_validate(prayer)


@router.get("/", response_model=PrayerListResponse)
async def get_prayers(
    status_filter: Optional[PrayerStatus] = Query(None, alias="status"),
    subject: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """기도 목록 조회"""
    prayers, total = await PrayerService.get_prayers(
        db=db,
        user_id=current_user.id,
        status=status_filter,
        subject=subject,
        search=search,
        page=page,
        limit=limit
    )
    
    # 각 기도에 progress_count와 prayer_days 추가
    prayers_with_progress = []
    for prayer in prayers:
        progress_count = await ProgressService.get_progress_count(db, prayer.id)
        prayer_days = PrayerService.calculate_prayer_days(prayer)
        
        prayer_dict = PrayerResponse.model_validate(prayer).model_dump()
        prayer_dict["progress_count"] = progress_count
        prayer_dict["prayer_days"] = prayer_days
        
        prayers_with_progress.append(PrayerWithProgress(**prayer_dict))
    
    pages = math.ceil(total / limit)
    
    return PrayerListResponse(
        items=prayers_with_progress,
        total=total,
        page=page,
        pages=pages
    )


@router.get("/{prayer_id}", response_model=PrayerResponse)
async def get_prayer(
    prayer_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """특정 기도 상세 조회"""
    prayer = await PrayerService.get_prayer_by_id(db, prayer_id, current_user.id)
    
    if not prayer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prayer not found"
        )
    
    return PrayerResponse.model_validate(prayer)


@router.patch("/{prayer_id}", response_model=PrayerResponse)
async def update_prayer(
    prayer_id: UUID,
    prayer_data: PrayerUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """기도 수정"""
    prayer = await PrayerService.update_prayer(db, prayer_id, current_user.id, prayer_data)
    
    if not prayer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prayer not found"
        )
    
    return PrayerResponse.model_validate(prayer)


@router.delete("/{prayer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prayer(
    prayer_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """기도 삭제"""
    success = await PrayerService.delete_prayer(db, prayer_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prayer not found"
        )
    
    return None


@router.post("/{prayer_id}/answer", response_model=PrayerResponse)
async def answer_prayer(
    prayer_id: UUID,
    answer_data: PrayerAnswer,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """최종 응답 기록"""
    prayer = await PrayerService.answer_prayer(db, prayer_id, current_user.id, answer_data)
    
    if not prayer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prayer not found"
        )
    
    return PrayerResponse.model_validate(prayer)
