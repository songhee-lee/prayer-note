from datetime import date, datetime, timedelta
from typing import Optional


def days_between(start_date: date, end_date: Optional[date] = None) -> int:
    """두 날짜 사이의 일수 계산 (시작일 포함)"""
    if end_date is None:
        end_date = date.today()
    
    delta = end_date - start_date
    return delta.days + 1


def format_date(dt: date) -> str:
    """날짜를 문자열로 포맷팅"""
    return dt.strftime("%Y-%m-%d")


def parse_date(date_str: str) -> date:
    """문자열을 날짜로 파싱"""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def is_today(dt: date) -> bool:
    """오늘 날짜인지 확인"""
    return dt == date.today()


def get_week_start(dt: Optional[date] = None) -> date:
    """주의 시작일 (월요일) 반환"""
    if dt is None:
        dt = date.today()
    
    return dt - timedelta(days=dt.weekday())


def get_month_start(dt: Optional[date] = None) -> date:
    """월의 시작일 반환"""
    if dt is None:
        dt = date.today()
    
    return date(dt.year, dt.month, 1)
