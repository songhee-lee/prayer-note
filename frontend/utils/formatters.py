"""데이터 포맷팅"""
from datetime import datetime, date
from typing import Optional


def format_date(date_obj: Optional[date]) -> str:
    """날짜 포맷팅"""
    if not date_obj:
        return "-"
    
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00')).date()
        except:
            return date_obj
    
    return date_obj.strftime("%Y년 %m월 %d일")


def format_datetime(datetime_obj: Optional[datetime]) -> str:
    """날짜시간 포맷팅"""
    if not datetime_obj:
        return "-"
    
    if isinstance(datetime_obj, str):
        try:
            datetime_obj = datetime.fromisoformat(datetime_obj.replace('Z', '+00:00'))
        except:
            return datetime_obj
    
    return datetime_obj.strftime("%Y년 %m월 %d일 %H:%M")


def calculate_prayer_days(start_date: date, end_date: Optional[date] = None) -> int:
    """기도 일수 계산"""
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00')).date()
    
    if end_date is None:
        end_date = date.today()
    elif isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00')).date()
    
    delta = end_date - start_date
    return delta.days + 1


def truncate_text(text: str, length: int = 100) -> str:
    """텍스트 자르기"""
    if not text:
        return ""
    
    if len(text) <= length:
        return text
    
    return text[:length] + "..."


def format_status(status: str) -> str:
    """상태 한글 변환"""
    from config.constants import PRAYER_STATUS
    return PRAYER_STATUS.get(status, status)


def get_status_emoji(status: str) -> str:
    """상태 이모지"""
    from config.constants import STATUS_COLORS
    return STATUS_COLORS.get(status, "")