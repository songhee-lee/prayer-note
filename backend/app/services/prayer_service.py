from typing import Optional, List
from uuid import UUID
from datetime import datetime, date
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.prayer import Prayer, PrayerStatus
from app.schemas.prayer import PrayerCreate, PrayerUpdate, PrayerAnswer


class PrayerService:
    """기도 관련 비즈니스 로직"""
    
    @staticmethod
    async def create_prayer(
        db: AsyncSession,
        user_id: UUID,
        prayer_data: PrayerCreate
    ) -> Prayer:
        """기도 생성"""
        prayer = Prayer(
            user_id=user_id,
            subject=prayer_data.subject,
            title=prayer_data.title,
            content=prayer_data.content,
            prayer_type=prayer_data.prayer_type,
            prayer_targets=prayer_data.prayer_targets,
            category_tags=prayer_data.category_tags,
            start_date=prayer_data.start_date,
            status=PrayerStatus.ACTIVE
        )
        
        db.add(prayer)
        await db.commit()
        await db.refresh(prayer)
        
        return prayer
    
    @staticmethod
    async def get_prayer_by_id(
        db: AsyncSession,
        prayer_id: UUID,
        user_id: UUID
    ) -> Optional[Prayer]:
        """특정 기도 조회"""
        result = await db.execute(
            select(Prayer)
            .options(selectinload(Prayer.progress_records))
            .where(
                and_(
                    Prayer.id == prayer_id,
                    Prayer.user_id == user_id
                )
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_prayers(
        db: AsyncSession,
        user_id: UUID,
        status: Optional[PrayerStatus] = None,
        subject: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 10
    ) -> tuple[List[Prayer], int]:
        """기도 목록 조회 (필터링 및 페이지네이션)"""
        # 기본 쿼리
        query = select(Prayer).where(Prayer.user_id == user_id)
        
        # 필터링
        if status:
            query = query.where(Prayer.status == status)
        
        if subject:
            query = query.where(Prayer.subject == subject)
        
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    Prayer.title.ilike(search_term),
                    Prayer.content.ilike(search_term)
                )
            )
        
        # 전체 개수 조회
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # 페이지네이션 및 정렬
        query = query.order_by(Prayer.created_at.desc())
        query = query.offset((page - 1) * limit).limit(limit)
        
        # 실행
        result = await db.execute(query)
        prayers = result.scalars().all()
        
        return list(prayers), total
    
    @staticmethod
    async def update_prayer(
        db: AsyncSession,
        prayer_id: UUID,
        user_id: UUID,
        prayer_data: PrayerUpdate
    ) -> Optional[Prayer]:
        """기도 수정"""
        prayer = await PrayerService.get_prayer_by_id(db, prayer_id, user_id)
        
        if not prayer:
            return None
        
        # 업데이트
        update_data = prayer_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(prayer, field, value)
        
        await db.commit()
        await db.refresh(prayer)
        
        return prayer
    
    @staticmethod
    async def delete_prayer(
        db: AsyncSession,
        prayer_id: UUID,
        user_id: UUID
    ) -> bool:
        """기도 삭제"""
        prayer = await PrayerService.get_prayer_by_id(db, prayer_id, user_id)
        
        if not prayer:
            return False
        
        await db.delete(prayer)
        await db.commit()
        
        return True
    
    @staticmethod
    async def answer_prayer(
        db: AsyncSession,
        prayer_id: UUID,
        user_id: UUID,
        answer_data: PrayerAnswer
    ) -> Optional[Prayer]:
        """최종 응답 기록"""
        prayer = await PrayerService.get_prayer_by_id(db, prayer_id, user_id)
        
        if not prayer:
            return None
        
        prayer.status = PrayerStatus.ANSWERED
        prayer.answer_date = answer_data.answer_date
        prayer.answer_content = answer_data.answer_content
        
        await db.commit()
        await db.refresh(prayer)
        
        return prayer
    
    @staticmethod
    def calculate_prayer_days(prayer: Prayer) -> int:
        """기도 일수 계산"""
        if prayer.status == PrayerStatus.ANSWERED and prayer.answer_date:
            end_date = prayer.answer_date
        else:
            end_date = date.today()
        
        delta = end_date - prayer.start_date
        return delta.days + 1  # 시작일 포함
