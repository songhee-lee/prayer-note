"""상수 정의"""

# 기도 주제
PRAYER_SUBJECTS = [
    "배우자",
    "가족",
    "건강",
    "진로/직장",
    "재정",
    "사역",
    "섬김",
    "관계",
    "영성",
    "직접 입력"
]

# 기도 유형
PRAYER_TYPES = [
    "감사",
    "간구",
    "회개",
    "중보",
    "직접 입력"
]

# 기도 상태
PRAYER_STATUS = {
    "in_progress": "진행 중",
    "answered": "응답받음"
}

# 상태 색상
STATUS_COLORS = {
    "in_progress": "🔵",
    "answered": "✅"
}

# 페이지네이션
ITEMS_PER_PAGE = 10

# 텍스트 길이 제한
MAX_TITLE_LENGTH = 200
MAX_CONTENT_LENGTH = 2000
MAX_ANSWER_LENGTH = 1000
MAX_LOG_LENGTH = 1000

# 정렬 옵션
SORT_OPTIONS = {
    "최신순": "created_at_desc",
    "오래된순": "created_at_asc",
    "시작일 최신순": "start_date_desc",
    "시작일 오래된순": "start_date_asc"
}