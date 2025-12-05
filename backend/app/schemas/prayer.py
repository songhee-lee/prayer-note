from datetime import datetime, date
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.prayer import PrayerStatus


# 기도 생성
class PrayerCreate(BaseModel):
    subject: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=2000)
    prayer_type: str = Field(..., min_length=1, max_length=50)
    prayer_targets: List[str] = Field(default_factory=list)
    category_tags: List[str] = Field(default_factory=list)
    start_date: date


# 기도 수정
class PrayerUpdate(BaseModel):
    subject: Optional[str] = Field(None, min_length=1, max_length=100)
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1, max_length=2000)
    prayer_type: Optional[str] = Field(None, min_length=1, max_length=50)
    prayer_targets: Optional[List[str]] = None
    category_tags: Optional[List[str]] = None
    start_date: Optional[date] = None


# 최종 응답 기록
class PrayerAnswer(BaseModel):
    answer_date: date
    answer_content: str = Field(..., min_length=1, max_length=1000)


# 기도 응답 (기본)
class PrayerResponse(BaseModel):
    id: UUID
    user_id: UUID
    subject: str
    title: str
    content: str
    prayer_type: str
    prayer_targets: List[str]
    category_tags: List[str]
    status: PrayerStatus
    start_date: date
    answer_date: Optional[date] = None
    answer_content: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


# 기도 응답 (응답 과정 포함)
class PrayerWithProgress(PrayerResponse):
    progress_count: int = 0
    prayer_days: int = 0


# 기도 목록 응답
class PrayerListResponse(BaseModel):
    items: List[PrayerWithProgress]
    total: int
    page: int
    pages: int
