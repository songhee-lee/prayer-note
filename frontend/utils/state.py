"""세션 상태 관리"""
import streamlit as st
from typing import Optional, Dict


def init_session_state():
    """세션 상태 초기화"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if "token" not in st.session_state:
        st.session_state.token = None
    
    if "user" not in st.session_state:
        st.session_state.user = None
    
    if "filters" not in st.session_state:
        st.session_state.filters = {}
    
    if "selected_prayer_id" not in st.session_state:
        st.session_state.selected_prayer_id = None


def is_authenticated() -> bool:
    """로그인 여부 확인"""
    return st.session_state.get("authenticated", False)


def get_current_user() -> Optional[Dict]:
    """현재 사용자 정보"""
    return st.session_state.get("user")


def save_token(token: str):
    """토큰 저장"""
    st.session_state.token = token
    st.session_state.authenticated = True


def get_token() -> Optional[str]:
    """토큰 조회"""
    return st.session_state.get("token")


def clear_session():
    """세션 클리어 (로그아웃)"""
    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.filters = {}
    st.session_state.selected_prayer_id = None