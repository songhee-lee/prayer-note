from typing import List, Dict
from pydantic import BaseModel
from app.schemas.prayer import PrayerWithProgress


# 주제별 통계
class SubjectStats(BaseModel):
    subject: str
    count: int


# 대시보드 통계
class DashboardStats(BaseModel):
    total_prayers: int
    active_prayers: int
    answered_prayers: int
    answer_rate: float
    by_subject: List[SubjectStats]


# 최근 기도 응답
class RecentPrayersResponse(BaseModel):
    items: List[PrayerWithProgress]
    total: int
