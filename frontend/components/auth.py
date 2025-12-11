"""인증 컴포넌트"""
import streamlit as st
from utils.api_client import api_client
from utils.state import save_token, clear_session


def validate_email(email: str) -> tuple[bool, str]:
    """이메일 형식 검증"""
    import re
    if not email:
        return False, "이메일을 입력해주세요."
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "올바른 이메일 형식이 아닙니다."
    
    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """비밀번호 검증"""
    if not password:
        return False, "비밀번호를 입력해주세요."
    
    if len(password) < 6:
        return False, "비밀번호는 최소 6자 이상이어야 합니다."
    
    return True, ""


def validate_username(username: str) -> tuple[bool, str]:
    """사용자명 검증"""
    if not username:
        return False, "사용자명을 입력해주세요."
    
    if len(username) < 2:
        return False, "사용자명은 최소 2자 이상이어야 합니다."
    
    return True, ""


def login_form():
    """로그인 폼"""
    st.subheader("🔐 로그인")

    with st.form("login_form"):
        email = st.text_input("이메일", placeholder="example@email.com")
        password = st.text_input("비밀번호", type="password")
        remember_me = st.checkbox("로그인 상태 유지", value=True, help="브라우저를 닫아도 로그인 상태가 유지됩니다 (30일간)")

        submitted = st.form_submit_button("로그인", use_container_width=True)

        if submitted:
            # 검증
            is_valid, error_msg = validate_email(email)
            if not is_valid:
                st.error(error_msg)
                return

            is_valid, error_msg = validate_password(password)
            if not is_valid:
                st.error(error_msg)
                return

            # API 호출
            try:
                with st.spinner("로그인 중..."):
                    response = api_client.login(email, password)

                    # 먼저 토큰을 세션에 저장
                    st.session_state.token = response["access_token"]
                    st.session_state.authenticated = True

                    # 사용자 정보 조회
                    user = api_client.get_current_user()
                    st.session_state.user = user

                    # 사용자 정보를 받은 후 파일에 저장
                    save_token(response["access_token"], remember_me=remember_me)

                    st.success("로그인 성공!")
                    st.rerun()
            except Exception as e:
                st.error(f"로그인 실패: {str(e)}")


def signup_form():
    """회원가입 폼"""
    st.subheader("✍️ 회원가입")
    
    with st.form("signup_form"):
        email = st.text_input("이메일", placeholder="example@email.com")
        username = st.text_input("사용자명", placeholder="홍길동")
        password = st.text_input("비밀번호", type="password")
        password_confirm = st.text_input("비밀번호 확인", type="password")
        
        submitted = st.form_submit_button("가입하기", use_container_width=True)
        
        if submitted:
            # 검증
            is_valid, error_msg = validate_email(email)
            if not is_valid:
                st.error(error_msg)
                return
            
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                st.error(error_msg)
                return
            
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                st.error(error_msg)
                return
            
            if password != password_confirm:
                st.error("비밀번호가 일치하지 않습니다.")
                return
            
            # API 호출
            try:
                with st.spinner("회원가입 중..."):
                    api_client.register(email, username, password)
                    st.success("회원가입 성공! 로그인해주세요.")
                    st.session_state.show_signup = False
                    st.rerun()
            except Exception as e:
                st.error(f"회원가입 실패: {str(e)}")


def logout_button():
    """로그아웃 버튼"""
    if st.button("🚪 로그아웃", use_container_width=True):
        clear_session()
        st.success("로그아웃되었습니다.")
        st.rerun()