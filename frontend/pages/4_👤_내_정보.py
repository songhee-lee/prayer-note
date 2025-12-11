"""내 정보 페이지"""
import streamlit as st
from utils.state import init_session_state, is_authenticated, get_current_user, try_auto_login
from components.auth import logout_button

# 페이지 설정
st.set_page_config(
    page_title="내 정보 - 기도 노트",
    page_icon="👤",
    layout="wide"
)

# 세션 상태 초기화
init_session_state()

# 자동 로그인 시도
try_auto_login()

# 인증 체크
if not is_authenticated():
    st.warning("로그인이 필요합니다.")
    st.switch_page("app.py")
    st.stop()

# 메인 컨텐츠
st.title("👤 내 정보")

user = get_current_user()

if user:
    # 사용자 정보 표시
    with st.container(border=True):
        st.subheader("📝 기본 정보")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**이메일:** {user.get('email', '-')}")
            st.markdown(f"**사용자명:** {user.get('username', '-')}")
        
        with col2:
            from utils.formatters import format_datetime
            st.markdown(f"**가입일:** {format_datetime(user.get('created_at', '-'))}")
    
    st.markdown("---")
    
    # 로그아웃
    st.subheader("🔐 계정 관리")
    logout_button()
    
    st.markdown("---")
    
    # 추가 정보
    st.info("""
    ### 📱 앱 정보
    - 버전: MVP 1.0
    - 문의: songhee172@gmail.com
    """)

else:
    st.error("사용자 정보를 불러올 수 없습니다.")
    if st.button("다시 로그인하기"):
        st.switch_page("app.py")