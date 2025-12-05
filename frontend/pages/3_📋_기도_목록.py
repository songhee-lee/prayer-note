"""기도 목록 페이지"""
import streamlit as st
from utils.state import init_session_state, is_authenticated
from utils.api_client import api_client
from components.filters import render_filters
from components.prayer_card import render_prayer_card
from components.prayer_log_form import render_log_form, render_log_list, render_answer_form

# 페이지 설정
st.set_page_config(
    page_title="기도 목록 - 기도 노트",
    page_icon="📋",
    layout="wide"
)

# 세션 상태 초기화
init_session_state()

# 인증 체크
if not is_authenticated():
    st.warning("로그인이 필요합니다.")
    st.switch_page("app.py")
    st.stop()

# 메인 컨텐츠
st.title("📋 기도 목록")

# 삭제 확인 처리
if "delete_prayer_id" in st.session_state and st.session_state.delete_prayer_id:
    prayer_id = st.session_state.delete_prayer_id
    
    st.warning("⚠️ 정말 이 기도를 삭제하시겠습니까?")
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        if st.button("삭제", type="primary", use_container_width=True):
            try:
                api_client.delete_prayer(prayer_id)
                st.success("기도가 삭제되었습니다.")
                st.session_state.delete_prayer_id = None
                st.rerun()
            except Exception as e:
                st.error(f"삭제 실패: {str(e)}")
    
    with col2:
        if st.button("취소", use_container_width=True):
            st.session_state.delete_prayer_id = None
            st.rerun()
    
    st.markdown("---")

# 필터링 UI
with st.expander("🔍 필터 및 검색", expanded=True):
    filters = render_filters()

# 기도 목록 로드
try:
    with st.spinner("기도 목록을 불러오는 중..."):
        prayers = api_client.get_prayers(
            status=filters.get("status"),
            subject=filters.get("subject"),
            search=filters.get("search"),
            sort_by=filters.get("sort_by")
        )
    
    # 결과 표시
    st.markdown(f"### 총 {len(prayers)}개의 기도")
    
    if not prayers:
        st.info("조건에 맞는 기도가 없습니다.")
    else:
        for prayer in prayers:
            render_prayer_card(prayer)
            
            # 응답 과정 기록 폼 표시
            if (st.session_state.get("show_log_form", False) and 
                st.session_state.get("selected_prayer_id") == prayer["id"]):
                
                with st.container(border=True):
                    render_log_form(prayer["id"])
            
            # 최종 응답 폼 표시
            if (st.session_state.get("show_answer_form", False) and 
                st.session_state.get("selected_prayer_id") == prayer["id"]):
                
                with st.container(border=True):
                    render_answer_form(prayer["id"])
            
            # 응답 과정 기록 목록 (expander로)
            if prayer.get("status") == "in_progress":
                with st.expander(f"📋 응답 과정 기록 보기"):
                    render_log_list(prayer["id"])
            
            st.markdown("---")

except Exception as e:
    st.error(f"기도 목록을 불러오는데 실패했습니다: {str(e)}")