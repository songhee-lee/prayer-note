"""기도 등록/수정 페이지"""
import streamlit as st
from utils.state import init_session_state, is_authenticated, try_auto_login
from utils.api_client import api_client
from components.prayer_form import render_prayer_form

# 페이지 설정
st.set_page_config(
    page_title="기도 등록 - 기도 노트",
    page_icon="✍️",
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


# 수정 모드 체크
is_edit_mode = st.session_state.get("edit_mode", False)
selected_prayer_id = st.session_state.get("selected_prayer_id")

if is_edit_mode and selected_prayer_id:
    # 수정 모드
    try:
        with st.spinner("기도 정보를 불러오는 중..."):
            prayer_data = api_client.get_prayer(selected_prayer_id)
        
        render_prayer_form(mode="edit", prayer_data=prayer_data)
    
    except Exception as e:
        st.error(f"기도 정보를 불러오는데 실패했습니다: {str(e)}")
        if st.button("목록으로 돌아가기"):
            st.session_state.edit_mode = False
            st.session_state.selected_prayer_id = None
            st.switch_page("pages/3_📋_기도_목록.py")
else:
    # 등록 모드
    render_prayer_form(mode="create")