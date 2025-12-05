"""통계 위젯 컴포넌트"""
import streamlit as st
from typing import Dict, List
import pandas as pd


def render_stat_cards(stats: Dict):
    """통계 카드 그리드"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📚 전체 기도",
            value=stats.get("total_prayers", 0)
        )
    
    with col2:
        st.metric(
            label="🔵 진행 중",
            value=stats.get("in_progress", 0)
        )
    
    with col3:
        st.metric(
            label="✅ 응답받음",
            value=stats.get("answered", 0)
        )
    
    with col4:
        answer_rate = stats.get("answer_rate", 0)
        st.metric(
            label="📊 응답률",
            value=f"{answer_rate:.1f}%"
        )


def render_subject_chart(subject_stats: List[Dict]):
    """주제별 통계 차트"""
    
    if not subject_stats:
        st.info("아직 기도 데이터가 없습니다.")
        return
    
    # 데이터 변환
    df = pd.DataFrame(subject_stats)
    
    if df.empty:
        st.info("통계 데이터가 없습니다.")
        return
    
    # 테이블로 표시
    st.subheader("📊 주제별 통계")
    
    # 데이터 정리
    df_display = df.copy()
    df_display.columns = ["주제", "진행 중", "응답받음", "전체"]
    
    # 전체 기준 내림차순 정렬
    df_display = df_display.sort_values("전체", ascending=False)
    
    st.dataframe(
        df_display,
        hide_index=True,
        use_container_width=True
    )
    
    # 간단한 바 차트
    st.bar_chart(df_display.set_index("주제")[["진행 중", "응답받음"]])


def render_simple_stats_row(stats: Dict):
    """간단한 통계 행 (대시보드용)"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**전체**: {stats.get('total_prayers', 0)}개")
    
    with col2:
        st.warning(f"**진행 중**: {stats.get('in_progress', 0)}개")
    
    with col3:
        st.success(f"**응답받음**: {stats.get('answered', 0)}개")