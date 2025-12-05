from typing import List, Dict
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.prayer import Prayer, PrayerStatus
from app.schemas.dashboard import SubjectStats


class StatsService:
    """통계 관련 비즈니스 로직"""
    
    @staticmethod
    async def get_dashboard_stats(db: AsyncSession, user_id: UUID) -> Dict:
        """대시보드 통계 조회"""
        # 전체 기도 개수
        total_result = await db.execute(
            select(func.count())
            .select_from(Prayer)
            .where(Prayer.user_id == user_id)
        )
        total_prayers = total_result.scalar()
        
        # 진행 중인 기도 개수
        active_result = await db.execute(
            select(func.count())
            .select_from(Prayer)
            .where(
                Prayer.user_id == user_id,
                Prayer.status == PrayerStatus.ACTIVE
            )
        )
        active_prayers = active_result.scalar()
        
        # 응답받은 기도 개수
        answered_result = await db.execute(
            select(func.count())
            .select_from(Prayer)
            .where(
                Prayer.user_id == user_id,
                Prayer.status == PrayerStatus.ANSWERED
            )
        )
        answered_prayers = answered_result.scalar()
        
        # 응답률 계산
        answer_rate = (answered_prayers / total_prayers * 100) if total_prayers > 0 else 0.0
        
        # 주제별 통계
        subject_result = await db.execute(
            select(
                Prayer.subject,
                func.count(Prayer.id).label("count")
            )
            .where(Prayer.user_id == user_id)
            .group_by(Prayer.subject)
            .order_by(func.count(Prayer.id).desc())
        )
        
        by_subject = [
            SubjectStats(subject=row.subject, count=row.count)
            for row in subject_result.all()
        ]
        
        return {
            "total_prayers": total_prayers,
            "active_prayers": active_prayers,
            "answered_prayers": answered_prayers,
            "answer_rate": round(answer_rate, 2),
            "by_subject": by_subject
        }
    
    @staticmethod
    async def get_recent_prayers(
        db: AsyncSession,
        user_id: UUID,
        limit: int = 5
    ) -> List[Prayer]:
        """최근 기도 목록"""
        result = await db.execute(
            select(Prayer)
            .where(Prayer.user_id == user_id)
            .order_by(Prayer.created_at.desc())
            .limit(limit)
        )
        
        return list(result.scalars().all())
