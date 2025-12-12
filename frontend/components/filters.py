"""필터링 컴포넌트"""
import streamlit as st
from typing import Dict
from config.constants import PRAYER_SUBJECTS, PRAYER_TYPES, SORT_OPTIONS


def render_filters() -> Dict:
    """필터링 UI 렌더링 및 필터 파라미터 반환"""
    
    st.markdown("##### 🔍 필터 및 검색")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 상태 필터
        status_filter = st.selectbox(
            "상태",
            options=["전체", "진행 중", "응답받음"],
            index=0
        )
        
        # 상태 값 매핑
        status_value = None
        if status_filter == "진행 중":
            status_value = "in_progress"
        elif status_filter == "응답받음":
            status_value = "answered"
    
    with col2:
        # 정렬
        sort_option = st.selectbox(
            "정렬",
            options=list(SORT_OPTIONS.keys()),
            index=0
        )
        sort_value = SORT_OPTIONS[sort_option]
    
    # 주제 필터
    subject_filter = st.multiselect(
        "주제",
        options=[s for s in PRAYER_SUBJECTS if s != "직접 입력"],
        default=[]
    )
    
    # 검색
    search_query = st.text_input(
        "검색",
        placeholder="제목 또는 내용 검색...",
        help="기도 제목이나 내용에서 검색합니다"
    )
    
    # 필터 파라미터 구성
    filters = {
        "status": status_value,
        "subject": subject_filter[0] if subject_filter else None,
        "search": search_query if search_query else None,
        "sort_by": sort_value
    }
    
    return filters