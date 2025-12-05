from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.prayer_progress import (
    ProgressCreate,
    ProgressUpdate,
    ProgressResponse,
    ProgressListResponse
)
from app.services.progress_service import ProgressService


router = APIRouter()


@router.get("/{prayer_id}/progress", response_model=ProgressListResponse)
async def get_progress_list(
    prayer_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """특정 기도의 응답 과정 목록"""
    progress_list = await ProgressService.get_progress_list(db, prayer_id, current_user.id)
    
    if progress_list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prayer not found"
        )
    
    return ProgressListResponse(
        items=[ProgressResponse.model_validate(p) for p in progress_list],
        total=len(progress_list)
    )


@router.post("/{prayer_id}/progress", response_model=ProgressResponse, status_code=status.HTTP_201_CREATED)
async def create_progress(
    prayer_id: UUID,
    progress_data: ProgressCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """응답 과정 추가"""
    progress = await ProgressService.create_progress(db, prayer_id, current_user.id, progress_data)
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prayer not found"
        )
    
    return ProgressResponse.model_validate(progress)


@router.patch("/progress/{progress_id}", response_model=ProgressResponse)
async def update_progress(
    progress_id: UUID,
    progress_data: ProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """응답 과정 수정"""
    progress = await ProgressService.update_progress(db, progress_id, current_user.id, progress_data)
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found"
        )
    
    return ProgressResponse.model_validate(progress)


@router.delete("/progress/{progress_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_progress(
    progress_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """응답 과정 삭제"""
    success = await ProgressService.delete_progress(db, progress_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found"
        )
    
    return None
