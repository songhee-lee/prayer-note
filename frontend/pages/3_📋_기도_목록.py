"""기도 목록 페이지"""
import streamlit as st
import pandas as pd
from datetime import date, datetime
from utils.state import init_session_state, is_authenticated, try_auto_login
from utils.api_client import api_client
from components.filters import render_filters

# 페이지 설정
st.set_page_config(
    page_title="기도 목록 - 기도 노트",
    page_icon="📋",
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
st.title("📋 기도 목록")

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
        # 데이터프레임으로 변환
        prayer_data = []
        for prayer in prayers:
            # 상태 이모지
            status_emoji = "✅" if prayer["status"] == "answered" else "🔵"

            prayer_data.append({
                "상태": status_emoji,
                "제목": prayer["title"],
                "주제": prayer["subject"],
                "유형": prayer["prayer_type"],
                "시작일": prayer["start_date"],
                "응답일": prayer.get("answer_date", "-"),
                "기도일수": prayer.get("prayer_days", 0),
                "id": prayer["id"]
            })

        df = pd.DataFrame(prayer_data)

        # 인덱스를 1부터 시작하도록 설정
        df.index = df.index + 1

        # 각 기도를 버튼으로 표시
        for idx in df.index:
            prayer = prayers[idx - 1]

            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                with col1:
                    st.markdown(f"**{df.loc[idx, '상태']} {df.loc[idx, '제목']}**")
                    st.caption(f"{df.loc[idx, '주제']} • {df.loc[idx, '유형']}")

                with col2:
                    st.caption("시작일")
                    st.text(df.loc[idx, '시작일'])

                with col3:
                    st.caption("기도일수")
                    st.text(f"{df.loc[idx, '기도일수']}일")

                with col4:
                    if st.button("상세보기", key=f"detail_{prayer['id']}", use_container_width=True):
                        st.session_state.selected_prayer_id = prayer['id']
                        st.session_state.show_prayer_detail = True
                        st.rerun()

        # 기도 상세 모달 (dialog로 표시)
        if st.session_state.get("show_prayer_detail") and st.session_state.get("selected_prayer_id"):
            prayer_id = st.session_state.selected_prayer_id

            # 기도 정보 로드
            with st.spinner("기도 정보를 불러오는 중..."):
                prayer = api_client.get_prayer(prayer_id)
                progress_logs = api_client.get_prayer_logs(prayer_id)

            # 모달 다이얼로그
            @st.dialog("📖 기도 상세", width="large")
            def show_prayer_detail():
                # 기도 기본 정보
                st.subheader(f"{prayer['title']}")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("주제", prayer["subject"])
                    st.metric("유형", prayer["prayer_type"])
                with col2:
                    st.metric("시작일", prayer["start_date"])
                    if prayer.get("answer_date"):
                        st.metric("응답일", prayer["answer_date"])
                with col3:
                    status_text = "✅ 응답받음" if prayer["status"] == "answered" else "🔵 진행중"
                    st.metric("상태", status_text)

                    # 기도 일수 계산
                    if prayer["status"] == "answered" and prayer.get("answer_date"):
                        end_date = datetime.strptime(prayer["answer_date"], "%Y-%m-%d").date()
                    else:
                        end_date = date.today()

                    start_date = datetime.strptime(prayer["start_date"], "%Y-%m-%d").date()
                    prayer_days = (end_date - start_date).days + 1
                    st.metric("기도 일수", f"{prayer_days}일")

                # 기도 내용
                st.markdown("### 기도 내용")
                st.markdown(f"> {prayer['content']}")

                # 기도 대상 및 태그
                if prayer.get("prayer_targets"):
                    st.markdown("**기도 대상:** " + ", ".join(prayer["prayer_targets"]))
                if prayer.get("category_tags"):
                    st.markdown("**카테고리:** " + ", ".join(prayer["category_tags"]))

                # 응답 내용 (있는 경우)
                if prayer["status"] == "answered":
                    st.markdown("---")
                    st.subheader("✨ 응답 내용")
                    if prayer.get("answer_content"):
                        st.success(prayer["answer_content"])
                    else:
                        st.warning("⚠️ 응답 받음으로 표시되었지만, 응답 내용이 작성되지 않았습니다.")

                        # 응답 내용 추가 폼
                        with st.form("add_answer_content"):
                            answer_content = st.text_area(
                                "응답 내용을 작성해주세요",
                                height=150,
                                placeholder="어떤 응답을 받으셨나요?"
                            )

                            if st.form_submit_button("응답 내용 저장", type="primary"):
                                try:
                                    api_client.mark_as_answered(prayer_id, {
                                        "answer_date": prayer["answer_date"],
                                        "answer_content": answer_content
                                    })
                                    st.success("응답 내용이 저장되었습니다!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"저장 실패: {str(e)}")

                st.markdown("---")

                # 응답 과정 기록
                st.subheader("📋 응답 과정 기록")

                # 새 기록 추가 폼
                with st.expander("➕ 새 기록 추가", expanded=False):
                    with st.form("add_progress"):
                        progress_content = st.text_area(
                            "기록 내용",
                            height=150,
                            placeholder="오늘의 기도 응답 과정을 기록해주세요..."
                        )

                        col1, col2 = st.columns([1, 4])
                        with col1:
                            if st.form_submit_button("등록", type="primary", use_container_width=True):
                                if not progress_content.strip():
                                    st.error("내용을 입력해주세요.")
                                else:
                                    try:
                                        api_client.create_prayer_log(prayer_id, {
                                            "content": progress_content,
                                            "recorded_date": date.today().isoformat()
                                        })
                                        st.success("기록이 추가되었습니다!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"등록 실패: {str(e)}")

                # 기존 기록 목록
                if progress_logs:
                    st.markdown(f"**총 {len(progress_logs)}개의 기록**")

                    for log in progress_logs:
                        with st.container(border=True):
                            col1, col2 = st.columns([4, 1])

                            with col1:
                                st.markdown(f"**{log['recorded_date']}**")

                                # 수정 모드
                                if st.session_state.get("edit_log_id") == log["id"]:
                                    with st.form(f"edit_log_{log['id']}"):
                                        edited_content = st.text_area(
                                            "내용 수정",
                                            value=log["content"],
                                            height=100,
                                            key=f"edit_content_{log['id']}"
                                        )

                                        col_a, col_b, col_c = st.columns([1, 1, 3])
                                        with col_a:
                                            if st.form_submit_button("저장", type="primary"):
                                                try:
                                                    api_client.update_prayer_log(
                                                        prayer_id,
                                                        log["id"],
                                                        {"content": edited_content}
                                                    )
                                                    st.session_state.edit_log_id = None
                                                    st.success("수정되었습니다!")
                                                    st.rerun()
                                                except Exception as e:
                                                    st.error(f"수정 실패: {str(e)}")

                                        with col_b:
                                            if st.form_submit_button("취소"):
                                                st.session_state.edit_log_id = None
                                                st.rerun()
                                else:
                                    st.markdown(log["content"])

                                    # 등록일/수정일 표시
                                    created_at = datetime.fromisoformat(log["created_at"].replace("Z", "+00:00"))
                                    updated_at = datetime.fromisoformat(log["updated_at"].replace("Z", "+00:00"))

                                    info_text = f"*등록: {created_at.strftime('%Y-%m-%d %H:%M')}*"
                                    if created_at != updated_at:
                                        info_text += f" | *수정: {updated_at.strftime('%Y-%m-%d %H:%M')}*"

                                    st.caption(info_text)

                            with col2:
                                if st.session_state.get("edit_log_id") != log["id"]:
                                    if st.button("✏️", key=f"edit_{log['id']}", use_container_width=True):
                                        st.session_state.edit_log_id = log["id"]
                                        st.rerun()

                                    if st.button("🗑️", key=f"delete_{log['id']}", use_container_width=True):
                                        try:
                                            api_client.delete_prayer_log(prayer_id, log["id"])
                                            st.success("삭제되었습니다!")
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"삭제 실패: {str(e)}")
                else:
                    st.info("아직 기록이 없습니다. 첫 기록을 추가해보세요!")

                # 응답 받음 처리 버튼 (진행중인 경우에만)
                if prayer["status"] != "answered":
                    st.markdown("---")
                    if st.button("✅ 응답 받음으로 표시", type="primary", use_container_width=True):
                        st.session_state.show_answer_modal = True
                        st.rerun()

                    # 응답 모달
                    if st.session_state.get("show_answer_modal"):
                        with st.form("answer_form"):
                            st.subheader("✨ 응답 받으셨나요?")

                            answer_date = st.date_input(
                                "응답 날짜",
                                value=date.today()
                            )

                            answer_content = st.text_area(
                                "응답 내용",
                                height=150,
                                placeholder="어떤 응답을 받으셨나요?"
                            )

                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("응답 등록", type="primary", use_container_width=True):
                                    if not answer_content.strip():
                                        st.error("응답 내용을 입력해주세요.")
                                    else:
                                        try:
                                            api_client.mark_as_answered(prayer_id, {
                                                "answer_date": answer_date.isoformat(),
                                                "answer_content": answer_content
                                            })
                                            st.session_state.show_answer_modal = False
                                            st.success("응답이 등록되었습니다!")
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"등록 실패: {str(e)}")

                            with col2:
                                if st.form_submit_button("취소", use_container_width=True):
                                    st.session_state.show_answer_modal = False
                                    st.rerun()

                # 닫기 버튼
                if st.button("닫기", use_container_width=True):
                    st.session_state.show_prayer_detail = False
                    st.session_state.selected_prayer_id = None
                    st.rerun()

            show_prayer_detail()

except Exception as e:
    st.error(f"기도 목록을 불러오는데 실패했습니다: {str(e)}")
