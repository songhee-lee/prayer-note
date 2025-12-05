import uuid
from datetime import datetime, date
from sqlalchemy import Column, Text, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base


class PrayerProgress(Base):
    """기도 응답 과정 기록 모델"""
    __tablename__ = "prayer_progress"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prayer_id = Column(UUID(as_uuid=True), ForeignKey("prayers.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 기록 내용
    content = Column(Text, nullable=False)
    recorded_date = Column(Date, nullable=False, index=True)
    tags = Column(JSONB, default=list, nullable=False)
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 관계
    prayer = relationship("Prayer", back_populates="progress_records")
    
    def __repr__(self):
        return f"<PrayerProgress(id={self.id}, prayer_id={self.prayer_id})>"
