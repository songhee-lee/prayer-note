"""대시보드 페이지"""
import streamlit as st
from utils.state import init_session_state, is_authenticated, try_auto_login
from utils.api_client import api_client
from components.stats import render_stat_cards, render_subject_chart
from components.prayer_card import render_prayer_card_simple

# 페이지 설정
st.set_page_config(
    page_title="대시보드 - 기도 노트",
    page_icon="🏠",
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
st.title("🏠 대시보드")

try:
    # 통계 데이터 로드
    with st.spinner("데이터를 불러오는 중..."):
        stats = api_client.get_dashboard_stats()
        subject_stats = api_client.get_subject_stats()
        recent_prayers = api_client.get_prayers(sort_by="created_at_desc", size=5)
        answered_without_content = api_client.get_answered_without_content()

    # 통계 카드
    render_stat_cards(stats)

    st.markdown("---")

    # 응답 내용 미작성 기도 경고
    if answered_without_content:
        st.warning(f"⚠️ 응답 받았지만 내용을 작성하지 않은 기도가 {len(answered_without_content)}개 있습니다!")

        with st.expander("📝 응답 내용 미작성 기도 목록", expanded=True):
            for prayer in answered_without_content:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{prayer['title']}** - {prayer['subject']}")
                    st.caption(f"응답일: {prayer.get('answer_date', 'N/A')}")
                with col2:
                    if st.button("작성하기", key=f"write_{prayer['id']}", use_container_width=True):
                        st.session_state.selected_prayer_id = prayer['id']
                        st.switch_page("pages/기도_상세.py")

        st.markdown("---")
    
    # 2단 레이아웃
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # 주제별 통계
        render_subject_chart(subject_stats)
    
    with col2:
        # 최근 기도 목록
        st.subheader("📝 최근 기도")
        
        if recent_prayers:
            for prayer in recent_prayers:
                render_prayer_card_simple(prayer)
        else:
            st.info("아직 등록된 기도가 없습니다.")
            if st.button("첫 기도 등록하기", type="primary"):
                st.switch_page("pages/2_✍️_기도_등록.py")

except Exception as e:
    st.error(f"데이터를 불러오는데 실패했습니다: {str(e)}")