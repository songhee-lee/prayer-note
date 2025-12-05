from typing import Optional, List
from uuid import UUID
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.prayer import Prayer
from app.models.prayer_progress import PrayerProgress
from app.schemas.prayer_progress import ProgressCreate, ProgressUpdate


class ProgressService:
    """응답 과정 관련 비즈니스 로직"""
    
    @staticmethod
    async def create_progress(
        db: AsyncSession,
        prayer_id: UUID,
        user_id: UUID,
        progress_data: ProgressCreate
    ) -> Optional[PrayerProgress]:
        """응답 과정 생성"""
        # 기도가 사용자 소유인지 확인
        prayer_result = await db.execute(
            select(Prayer).where(
                and_(
                    Prayer.id == prayer_id,
                    Prayer.user_id == user_id
                )
            )
        )
        prayer = prayer_result.scalar_one_or_none()
        
        if not prayer:
            return None
        
        progress = PrayerProgress(
            prayer_id=prayer_id,
            content=progress_data.content,
            recorded_date=progress_data.recorded_date,
            tags=progress_data.tags
        )
        
        db.add(progress)
        await db.commit()
        await db.refresh(progress)
        
        return progress
    
    @staticmethod
    async def get_progress_list(
        db: AsyncSession,
        prayer_id: UUID,
        user_id: UUID
    ) -> Optional[List[PrayerProgress]]:
        """특정 기도의 응답 과정 목록 조회"""
        # 기도가 사용자 소유인지 확인
        prayer_result = await db.execute(
            select(Prayer).where(
                and_(
                    Prayer.id == prayer_id,
                    Prayer.user_id == user_id
                )
            )
        )
        prayer = prayer_result.scalar_one_or_none()
        
        if not prayer:
            return None
        
        # 응답 과정 조회
        result = await db.execute(
            select(PrayerProgress)
            .where(PrayerProgress.prayer_id == prayer_id)
            .order_by(PrayerProgress.recorded_date.desc())
        )
        
        return list(result.scalars().all())
    
    @staticmethod
    async def get_progress_by_id(
        db: AsyncSession,
        progress_id: UUID,
        user_id: UUID
    ) -> Optional[PrayerProgress]:
        """특정 응답 과정 조회"""
        result = await db.execute(
            select(PrayerProgress)
            .join(Prayer)
            .where(
                and_(
                    PrayerProgress.id == progress_id,
                    Prayer.user_id == user_id
                )
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_progress(
        db: AsyncSession,
        progress_id: UUID,
        user_id: UUID,
        progress_data: ProgressUpdate
    ) -> Optional[PrayerProgress]:
        """응답 과정 수정"""
        progress = await ProgressService.get_progress_by_id(db, progress_id, user_id)
        
        if not progress:
            return None
        
        # 업데이트
        update_data = progress_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(progress, field, value)
        
        await db.commit()
        await db.refresh(progress)
        
        return progress
    
    @staticmethod
    async def delete_progress(
        db: AsyncSession,
        progress_id: UUID,
        user_id: UUID
    ) -> bool:
        """응답 과정 삭제"""
        progress = await ProgressService.get_progress_by_id(db, progress_id, user_id)
        
        if not progress:
            return False
        
        await db.delete(progress)
        await db.commit()
        
        return True
    
    @staticmethod
    async def get_progress_count(
        db: AsyncSession,
        prayer_id: UUID
    ) -> int:
        """특정 기도의 응답 과정 개수"""
        result = await db.execute(
            select(func.count())
            .select_from(PrayerProgress)
            .where(PrayerProgress.prayer_id == prayer_id)
        )
        return result.scalar()
