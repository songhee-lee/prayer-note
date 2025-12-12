"""응답 과정 기록 폼 컴포넌트"""
import streamlit as st
from datetime import date
from typing import Dict, List
from utils.api_client import api_client
from utils.formatters import format_date


def render_log_form(prayer_id: str):
    """응답 과정 기록 추가 폼"""
    
    st.markdown("##### 📝 응답 과정 기록 추가")
    
    with st.form("prayer_log_form", clear_on_submit=True):
        log_date = st.date_input(
            "날짜 *",
            value=date.today(),
            help="기록 날짜를 선택하세요"
        )
        
        content = st.text_area(
            "내용 *",
            height=150,
            max_chars=1000,
            placeholder="오늘 기도하면서 느낀 점, 변화, 하나님의 응답 등을 자유롭게 기록하세요...",
            help="마크다운 문법을 사용할 수 있습니다 (최대 1000자)"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button(
                "기록 추가",
                type="primary",
                use_container_width=True
            )
        with col2:
            cancelled = st.form_submit_button(
                "취소",
                use_container_width=True
            )
        
        if cancelled:
            st.session_state.show_log_form = False
            st.rerun()
        
        if submitted:
            if not content:
                st.error("내용을 입력해주세요.")
                return
            
            # API 호출
            try:
                with st.spinner("저장 중..."):
                    data = {
                        "recorded_date": log_date.isoformat(),
                        "content": content,
                        "tags": []
                    }
                    api_client.create_prayer_log(prayer_id, data)
                    st.success("응답 과정이 기록되었습니다!")
                    st.session_state.show_log_form = False
                    st.rerun()
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")


def render_log_list(prayer_id: str):
    """응답 과정 기록 목록"""
    
    try:
        logs = api_client.get_prayer_logs(prayer_id)
        
        if not logs:
            st.info("아직 응답 과정 기록이 없습니다.")
            return
        
        st.markdown(f"##### 📋 응답 과정 기록 ({len(logs)}개)")

        # 최신순 정렬
        logs_sorted = sorted(logs, key=lambda x: x["recorded_date"], reverse=True)

        for log in logs_sorted:
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{format_date(log['recorded_date'])}**")
                with col2:
                    if st.button("🗑️", key=f"delete_log_{log['id']}", help="삭제"):
                        if st.session_state.get(f"confirm_delete_log_{log['id']}", False):
                            try:
                                api_client.delete_prayer_log(prayer_id, log["id"])
                                st.success("기록이 삭제되었습니다.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"삭제 실패: {str(e)}")
                        else:
                            st.session_state[f"confirm_delete_log_{log['id']}"] = True
                            st.warning("한 번 더 클릭하면 삭제됩니다.")
                
                st.write(log["content"])
                st.caption(f"작성일: {format_date(log['created_at'])}")
        
    except Exception as e:
        st.error(f"기록을 불러오는데 실패했습니다: {str(e)}")


def render_answer_form(prayer_id: str):
    """최종 응답 기록 폼"""
    
    st.markdown("##### ✅ 기도 응답 처리")
    
    with st.form("answer_form"):
        answered_date = st.date_input(
            "응답 날짜 *",
            value=date.today(),
            help="기도가 응답된 날짜를 선택하세요"
        )
        
        answer_content = st.text_area(
            "응답 내용 *",
            height=150,
            max_chars=1000,
            placeholder="어떻게 응답받으셨나요? 하나님께서 어떤 방식으로 기도에 답하셨는지 기록하세요...",
            help="최대 1000자"
        )
        
        thanks_note = st.text_area(
            "감사 노트 (선택)",
            height=100,
            max_chars=500,
            placeholder="하나님께 드리는 감사의 마음을 표현해보세요...",
            help="최대 500자"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button(
                "응답 완료 처리",
                type="primary",
                use_container_width=True
            )
        with col2:
            cancelled = st.form_submit_button(
                "취소",
                use_container_width=True
            )
        
        if cancelled:
            st.session_state.show_answer_form = False
            st.rerun()
        
        if submitted:
            if not answer_content:
                st.error("응답 내용을 입력해주세요.")
                return
            
            # API 호출
            try:
                with st.spinner("저장 중..."):
                    data = {
                        "answer_date": answered_date.isoformat(),
                        "answer_content": answer_content
                    }
                    api_client.mark_as_answered(prayer_id, data)
                    st.success("기도가 응답 완료 처리되었습니다! 🎉")
                    st.session_state.show_answer_form = False
                    st.session_state.selected_prayer_id = None
                    st.rerun()
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")