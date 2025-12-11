"""세션 상태 관리"""
import streamlit as st
from typing import Optional, Dict
import json
import os
from pathlib import Path


# 세션 파일 경로
SESSION_DIR = Path.home() / ".prayer_note"
SESSION_FILE = SESSION_DIR / "session.json"


def _ensure_session_dir():
    """세션 디렉토리 생성"""
    SESSION_DIR.mkdir(parents=True, exist_ok=True)


def _load_saved_session() -> Optional[Dict]:
    """저장된 세션 로드"""
    try:
        if SESSION_FILE.exists():
            with open(SESSION_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"세션 로드 실패: {e}")
    return None


def _save_session_to_file(token: str, user: Dict):
    """세션을 파일에 저장"""
    try:
        _ensure_session_dir()
        session_data = {
            "token": token,
            "user": user
        }
        with open(SESSION_FILE, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"세션 저장 실패: {e}")


def _clear_session_file():
    """세션 파일 삭제"""
    try:
        if SESSION_FILE.exists():
            SESSION_FILE.unlink()
    except Exception as e:
        print(f"세션 파일 삭제 실패: {e}")


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


def is_authenticated() -> bool:
    """로그인 여부 확인"""
    return st.session_state.get("authenticated", False)


def get_current_user() -> Optional[Dict]:
    """현재 사용자 정보"""
    return st.session_state.get("user")


def save_token(token: str, remember_me: bool = True):
    """토큰을 파일에 저장 (세션 상태는 이미 설정되어 있어야 함)"""
    st.session_state.remember_me = remember_me

    # remember_me가 True면 파일에 저장
    if remember_me and st.session_state.get("user"):
        _save_session_to_file(token, st.session_state.user)


def get_token() -> Optional[str]:
    """토큰 조회"""
    return st.session_state.get("token")


def clear_session():
    """세션 클리어 (로그아웃)"""
    _clear_session_file()

    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.filters = {}
    st.session_state.selected_prayer_id = None
    st.session_state.auto_login_attempted = False


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

    # 저장된 세션 로드
    saved_session = _load_saved_session()

    if not saved_session:
        return False

    token = saved_session.get("token")
    saved_user = saved_session.get("user")

    if not token or not saved_user:
        _clear_session_file()
        return False

    # 토큰으로 사용자 정보 조회하여 유효성 검증
    try:
        # 먼저 토큰을 세션에 설정
        st.session_state.token = token

        # API로 사용자 정보 검증
        user = api_client.get_current_user()

        # 사용자 ID가 같은지 확인
        if user.get("id") == saved_user.get("id"):
            st.session_state.user = user
            st.session_state.authenticated = True
            # 디버깅: 자동 로그인 성공 메시지
            print(f"✅ 자동 로그인 성공: {user.get('email')}")
            return True
        else:
            # 사용자가 다르면 세션 파일 삭제
            print(f"❌ 사용자 불일치: 저장된 ID={saved_user.get('id')}, 현재 ID={user.get('id')}")
            _clear_session_file()
            st.session_state.token = None
            st.session_state.authenticated = False
            return False
    except Exception as e:
        # 토큰이 유효하지 않으면 세션 파일 삭제
        print(f"❌ 자동 로그인 실패: {str(e)}")
        _clear_session_file()
        st.session_state.token = None
        st.session_state.authenticated = False
        return False
