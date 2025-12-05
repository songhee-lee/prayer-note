from datetime import datetime, date
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field


# 응답 과정 생성
class ProgressCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    recorded_date: date
    tags: List[str] = Field(default_factory=list)


# 응답 과정 수정
class ProgressUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=2000)
    recorded_date: Optional[date] = None
    tags: Optional[List[str]] = None


# 응답 과정 응답
class ProgressResponse(BaseModel):
    id: UUID
    prayer_id: UUID
    content: str
    recorded_date: date
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


# 응답 과정 목록
class ProgressListResponse(BaseModel):
    items: List[ProgressResponse]
    total: int
