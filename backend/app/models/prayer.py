import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Text, Date, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class PrayerStatus(str, enum.Enum):
    """기도 상태"""
    ACTIVE = "active"
    ANSWERED = "answered"


class Prayer(Base):
    """기도 모델"""
    __tablename__ = "prayers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 기본 정보
    subject = Column(String(100), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    prayer_type = Column(String(50), nullable=False)
    
    # JSON 배열 필드
    prayer_targets = Column(JSONB, default=list, nullable=False)
    category_tags = Column(JSONB, default=list, nullable=False)
    
    # 상태 및 날짜
    status = Column(SQLEnum(PrayerStatus), default=PrayerStatus.ACTIVE, nullable=False, index=True)
    start_date = Column(Date, nullable=False, index=True)
    answer_date = Column(Date, nullable=True)
    answer_content = Column(Text, nullable=True)
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 관계
    user = relationship("User", back_populates="prayers")
    progress_records = relationship("PrayerProgress", back_populates="prayer", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Prayer(id={self.id}, title={self.title}, status={self.status})>"
