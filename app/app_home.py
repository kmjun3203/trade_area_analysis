import streamlit as st
from pathlib import Path


def run_home():
    st.title("서울 상권 분석 대시보드")
    
    # 메인 소개
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 30px; border-radius: 10px; margin-bottom: 30px;'>
        <h3 style='color: #1f77b4; margin-bottom: 20px;'>서울시 상권 데이터를 기반으로</h3>
        <p style='font-size: 18px; line-height: 1.8;'>
            ✔ 사람들이 많은지<br>
            ✔ 경쟁이 심하지 않은지<br>
            ✔ 앞으로도 괜찮을지<br>
            <strong>를 분석해 창업 판단을 돕는 서비스입니다</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 사용 방법
    st.markdown("### 🧭 사용 방법")
    st.info("""
    **① 사이드바에서 상권과 업종을 선택하세요**
    
    **② 상권 분석 → 시장 분석 → 미래 판단 순서로 확인하세요**
    
    **③ 최종 창업 적합도 점수를 확인하세요**
    """)
    
    # 추천 대상
    st.markdown("### 👤 이런 분들께 추천합니다")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background-color: #e8f4f8; padding: 20px; border-radius: 10px; text-align: center;'>
            <p>자영업 창업을<br>고민 중인 분</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #e8f4f8; padding: 20px; border-radius: 10px; text-align: center;'>
            <p>상권 비교를<br>데이터로 하고 싶은 분</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background-color: #e8f4f8; padding: 20px; border-radius: 10px; text-align: center;'>
            <p>감이 아니라<br>근거로 결정하고 싶은 분</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
