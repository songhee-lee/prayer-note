import streamlit as st
import sys
from pathlib import Path

# 현재 디렉토리를 Python 경로에 추가
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from utils.state import init_session_state, is_authenticated
from components.auth import login_form, signup_form

# 페이지 설정
st.set_page_config(
    page_title="기도 노트",
    page_icon="🙏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
init_session_state()

# 커스텀 CSS
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #4F46E5;
    }
    .subtitle {
        text-align: center;
        color: #6B7280;
        margin-bottom: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# 로그인/로그아웃 페이지 정의
def login_page():
    st.markdown('<h1 class="main-title">🙏 기도 노트</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">하나님께 드리는 기도를 기록하고 응답을 경험하세요</p>', unsafe_allow_html=True)

    # 탭으로 로그인/회원가입 구분
    tab1, tab2 = st.tabs(["로그인", "회원가입"])

    with tab1:
        login_form()

    with tab2:
        signup_form()

    # 하단 안내
    st.markdown("---")
    st.markdown("""
    ### 📖 기도 노트란?
    - 📝 기도 제목을 체계적으로 기록하고 관리
    - 📊 기도 응답 과정을 추적하고 통계 확인
    - ✅ 응답받은 기도를 통해 하나님의 신실하심을 경험
    """)

def logout():
    if st.button("로그아웃"):
        st.session_state.clear()
        st.rerun()

# 페이지 객체 생성
login_pg = st.Page(login_page, title="로그인", icon="🔐")
logout_pg = st.Page(logout, title="로그아웃", icon="👋")

# 로그인 상태에 따른 네비게이션 설정
if not is_authenticated():
    # 로그아웃 상태 - 로그인 페이지만 표시
    pg = st.navigation([login_pg])
else:
    # 로그인 상태 - 전체 네비게이션 표시
    pg = st.navigation({
        "계정": [logout_pg],
        "메뉴": [
            st.Page("./pages/1_🏠_대시보드.py", title="대시보드", icon="🏠"),
            st.Page("./pages/2_✍️_기도_등록.py", title="기도 등록", icon="✍️"),
            st.Page("./pages/3_📋_기도_목록.py", title="기도 목록", icon="📋"),
            st.Page("./pages/4_👤_내_정보.py", title="내 정보", icon="👤"),
        ]
    })

pg.run()