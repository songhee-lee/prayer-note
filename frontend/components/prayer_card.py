"""기도 카드 컴포넌트"""
import streamlit as st
from typing import Dict
from utils.formatters import (
    format_date, 
    calculate_prayer_days, 
    truncate_text,
    format_status,
    get_status_emoji
)


def render_prayer_card(prayer: Dict, show_actions: bool = True):
    """기도 카드 렌더링"""
    
    # 상태 정보
    status = prayer.get("status", "in_progress")
    status_text = format_status(status)
    status_emoji = get_status_emoji(status)
    
    # 기도 일수 계산
    start_date = prayer.get("start_date")
    answered_date = prayer.get("answered_date")
    prayer_days = calculate_prayer_days(start_date, answered_date)
    
    # 카드 컨테이너
    with st.container(border=True):
        # 헤더 (제목 + 상태)
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"##### {prayer.get('title', '제목 없음')}")
        with col2:
            st.markdown(f"{status_emoji} **{status_text}**")
        
        # 기본 정보
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption(f"**주제:** {prayer.get('subject', '-')}")
        with col2:
            st.caption(f"**유형:** {prayer.get('prayer_type', '-')}")
        with col3:
            st.caption(f"**기도 일수:** {prayer_days}일")
        
        # 날짜 정보
        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"**시작일:** {format_date(start_date)}")
        with col2:
            if answered_date:
                st.caption(f"**응답일:** {format_date(answered_date)}")
        
        # 내용 미리보기
        content = prayer.get("content", "")
        if content:
            with st.expander("📝 기도 내용 보기"):
                st.write(content)
        
        # 응답 내용 (있을 경우)
        if prayer.get("answer_content"):
            with st.expander("✅ 응답 내용 보기"):
                st.write(prayer.get("answer_content"))
                if prayer.get("thanks_note"):
                    st.markdown("**감사 노트:**")
                    st.write(prayer.get("thanks_note"))
        
        # 액션 버튼
        if show_actions:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("📝 수정", key=f"edit_{prayer['id']}", use_container_width=True):
                    st.session_state.selected_prayer_id = prayer["id"]
                    st.session_state.edit_mode = True
                    st.switch_page("pages/2_✍️_기도_등록.py")
            
            with col2:
                if st.button("🗑️ 삭제", key=f"delete_{prayer['id']}", use_container_width=True):
                    st.session_state.delete_prayer_id = prayer["id"]
                    st.rerun()
            
            with col3:
                if status == "in_progress":
                    if st.button("📋 기록", key=f"log_{prayer['id']}", use_container_width=True):
                        st.session_state.selected_prayer_id = prayer["id"]
                        st.session_state.show_log_form = True
                        st.rerun()
            
            with col4:
                if status == "in_progress":
                    if st.button("✅ 응답", key=f"answer_{prayer['id']}", use_container_width=True):
                        st.session_state.selected_prayer_id = prayer["id"]
                        st.session_state.show_answer_form = True
                        st.rerun()


def render_prayer_card_simple(prayer: Dict):
    """간단한 기도 카드 (대시보드용)"""
    status_emoji = get_status_emoji(prayer.get("status", "in_progress"))
    
    with st.container(border=True):
        st.markdown(f"{status_emoji} **{prayer.get('title', '제목 없음')}**")
        st.caption(f"{prayer.get('subject', '-')} | {format_date(prayer.get('start_date'))}")