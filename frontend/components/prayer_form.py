"""기도 폼 컴포넌트"""
import streamlit as st
from datetime import date, datetime
from typing import Optional, Dict
from config.constants import PRAYER_SUBJECTS, PRAYER_TYPES
from utils.api_client import api_client


def validate_prayer_form(data: dict) -> tuple[bool, str]:
    """기도 폼 데이터 검증"""
    if not data.get("subject"):
        return False, "주제를 선택해주세요."
    
    if not data.get("title"):
        return False, "기도 제목을 입력해주세요."
    
    if len(data.get("title", "")) > 200:
        return False, "기도 제목은 200자 이하로 입력해주세요."
    
    if not data.get("content"):
        return False, "기도 내용을 입력해주세요."
    
    if len(data.get("content", "")) > 2000:
        return False, "기도 내용은 2000자 이하로 입력해주세요."
    
    if not data.get("prayer_type"):
        return False, "기도 유형을 선택해주세요."
    
    if not data.get("start_date"):
        return False, "시작 날짜를 선택해주세요."
    
    return True, ""


def render_prayer_form(mode: str = "create", prayer_data: Optional[Dict] = None):
    """기도 등록/수정 폼
    
    Args:
        mode: 'create' 또는 'edit'
        prayer_data: 수정 모드일 때 기존 기도 데이터
    """
    
    is_edit = mode == "edit" and prayer_data is not None
    form_title = "✏️ 기도 수정" if is_edit else "✍️ 새 기도 등록"
    
    st.subheader(form_title)
    
    with st.form("prayer_form", clear_on_submit=not is_edit):
        # 주제 선택
        subject_index = 0
        if is_edit and prayer_data.get("subject"):
            try:
                subject_index = PRAYER_SUBJECTS.index(prayer_data["subject"])
            except ValueError:
                subject_index = len(PRAYER_SUBJECTS) - 1  # "직접 입력"
        
        subject = st.selectbox(
            "주제 *",
            options=PRAYER_SUBJECTS,
            index=subject_index,
            help="기도의 주제를 선택하세요"
        )
        
        # 직접 입력
        custom_subject = None
        if subject == "직접 입력":
            custom_subject = st.text_input(
                "주제 직접 입력 *",
                value=prayer_data.get("subject", "") if is_edit and prayer_data.get("subject") not in PRAYER_SUBJECTS else "",
                placeholder="예: 친구의 건강"
            )
            if custom_subject:
                subject = custom_subject
        
        # 기도 제목
        title = st.text_input(
            "기도 제목 *",
            value=prayer_data.get("title", "") if is_edit else "",
            max_chars=200,
            placeholder="예: 좋은 배우자를 만나게 해주세요",
            help="간결하고 명확한 제목을 입력하세요 (최대 200자)"
        )
        
        # 기도 내용
        content = st.text_area(
            "기도 내용 *",
            value=prayer_data.get("content", "") if is_edit else "",
            height=200,
            max_chars=2000,
            placeholder="구체적인 기도 내용을 자유롭게 작성하세요...",
            help="마크다운 문법을 사용할 수 있습니다 (최대 2000자)"
        )
        
        # 기도 유형
        prayer_type_index = 0
        if is_edit and prayer_data.get("prayer_type"):
            try:
                prayer_type_index = PRAYER_TYPES.index(prayer_data["prayer_type"])
            except ValueError:
                prayer_type_index = len(PRAYER_TYPES) - 1  # "직접 입력"
        
        prayer_type = st.selectbox(
            "기도 유형 *",
            options=PRAYER_TYPES,
            index=prayer_type_index,
            help="기도의 유형을 선택하세요"
        )
        
        # 직접 입력
        custom_type = None
        if prayer_type == "직접 입력":
            custom_type = st.text_input(
                "기도 유형 직접 입력 *",
                value=prayer_data.get("prayer_type", "") if is_edit and prayer_data.get("prayer_type") not in PRAYER_TYPES else "",
                placeholder="예: 찬양"
            )
            if custom_type:
                prayer_type = custom_type
        
        # 시작 날짜
        start_date_value = date.today()
        if is_edit and prayer_data.get("start_date"):
            try:
                if isinstance(prayer_data["start_date"], str):
                    start_date_value = datetime.fromisoformat(
                        prayer_data["start_date"].replace('Z', '+00:00')
                    ).date()
                else:
                    start_date_value = prayer_data["start_date"]
            except:
                pass
        
        start_date = st.date_input(
            "시작 날짜 *",
            value=start_date_value,
            help="기도를 시작한 날짜를 선택하세요"
        )
        
        # 제출 버튼
        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button(
                "수정하기" if is_edit else "등록하기",
                type="primary",
                use_container_width=True
            )
        with col2:
            cancelled = st.form_submit_button(
                "취소",
                use_container_width=True
            )
        
        if cancelled:
            st.session_state.edit_mode = False
            st.session_state.selected_prayer_id = None
            st.switch_page("pages/3_📋_기도_목록.py")
        
        if submitted:
            # 폼 데이터 구성
            form_data = {
                "subject": subject,
                "title": title,
                "content": content,
                "prayer_type": prayer_type,
                "prayer_targets": [],
                "category_tags": [],
                "start_date": start_date.isoformat()
            }
            
            # 검증
            is_valid, error_msg = validate_prayer_form(form_data)
            if not is_valid:
                st.error(error_msg)
                return
            
            # API 호출
            try:
                with st.spinner("저장 중..."):
                    if is_edit:
                        api_client.update_prayer(prayer_data["id"], form_data)
                        st.success("기도가 수정되었습니다!")
                    else:
                        api_client.create_prayer(form_data)
                        st.success("기도가 등록되었습니다!")
                    
                    # 상태 초기화
                    st.session_state.edit_mode = False
                    st.session_state.selected_prayer_id = None
                    
                    # 목록 페이지로 이동
                    st.switch_page("pages/3_📋_기도_목록.py")
                    
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")