"""세션 상태 관리"""
import streamlit as st
from typing import Optional, Dict
import extra_streamlit_components as stx


def get_cookie_manager():
    """쿠키 관리자 가져오기"""
    return stx.CookieManager()


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

    if "auto_login_attempted" not in st.session_state:
        st.session_state.auto_login_attempted = False

    if "remember_me" not in st.session_state:
        st.session_state.remember_me = True

    if "cookie_manager" not in st.session_state:
        st.session_state.cookie_manager = get_cookie_manager()


def is_authenticated() -> bool:
    """로그인 여부 확인"""
    return st.session_state.get("authenticated", False)


def get_current_user() -> Optional[Dict]:
    """현재 사용자 정보"""
    return st.session_state.get("user")


def save_token(token: str, remember_me: bool = True):
    """토큰 저장 (세션 및 쿠키)"""
    st.session_state.token = token
    st.session_state.authenticated = True
    st.session_state.remember_me = remember_me

    # remember_me가 True면 쿠키에 저장 (30일 유지)
    if remember_me:
        try:
            cookie_manager = st.session_state.cookie_manager
            cookie_manager.set("prayer_note_token", token, max_age=30*24*60*60)
        except Exception as e:
            print(f"쿠키 저장 실패: {e}")


def get_token() -> Optional[str]:
    """토큰 조회"""
    return st.session_state.get("token")


def clear_session():
    """세션 클리어 (로그아웃)"""
    try:
        cookie_manager = st.session_state.cookie_manager
        cookie_manager.delete("prayer_note_token")
    except Exception as e:
        print(f"쿠키 삭제 실패: {e}")

    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.filters = {}
    st.session_state.selected_prayer_id = None
    st.session_state.auto_login_attempted = False


def load_token_from_cookie() -> Optional[str]:
    """쿠키에서 토큰 로드"""
    try:
        cookie_manager = st.session_state.cookie_manager
        all_cookies = cookie_manager.get_all()
        return all_cookies.get("prayer_note_token")
    except Exception as e:
        print(f"쿠키 로드 실패: {e}")
        return None


def try_auto_login() -> bool:
    """저장된 토큰으로 자동 로그인 시도"""
    from utils.api_client import api_client

    # 이미 로그인되어 있으면 스킵
    if st.session_state.authenticated:
        return True

    # 이미 자동 로그인을 시도했으면 스킵
    if st.session_state.auto_login_attempted:
        return st.session_state.authenticated

    st.session_state.auto_login_attempted = True

    # 쿠키에서 토큰 로드
    stored_token = load_token_from_cookie()

    if not stored_token:
        return False

    # 토큰으로 사용자 정보 조회 시도
    try:
        st.session_state.token = stored_token
        user = api_client.get_current_user()
        st.session_state.user = user
        st.session_state.authenticated = True
        return True
    except Exception as e:
        # 토큰이 유효하지 않으면 쿠키 삭제
        print(f"자동 로그인 실패: {e}")
        try:
            cookie_manager = st.session_state.cookie_manager
            cookie_manager.delete("prayer_note_token")
        except:
            pass
        st.session_state.token = None
        st.session_state.authenticated = False
        return False
