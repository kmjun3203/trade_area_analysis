# components/sidebar.py
import streamlit as st
import os
import base64
import pandas as pd
from pathlib import Path


# 데이터 디렉토리 경로
DATA_DIR = Path(__file__).parent.parent.parent / "data"


@st.cache_data
def load_area_data():
    """영역 데이터 로드"""
    filepath = DATA_DIR / "서울시 상권분석서비스(영역-상권)_filtered.csv"
    return pd.read_csv(filepath, encoding='cp949')


@st.cache_data
def load_stores_data():
    """점포 데이터 로드"""
    filepath = DATA_DIR / "서울시 상권분석서비스(점포-상권)_filtered.csv"
    return pd.read_csv(filepath, encoding='cp949')


def render_sidebar():
    """사이드바 렌더링: 메뉴 + 필터 + 로고"""
    
    with st.sidebar:
        # 메뉴 선택
        st.title("Menu")
        menu = ['홈 화면', '상권 개요', '시장 환경', '상권 전망']
        choice = st.selectbox('선택', menu)
        
        st.divider()
        
        # 상권/업종 선택
        st.subheader("분석 대상 선택")
        
        # 데이터 로드
        area_df = load_area_data()
        stores_df = load_stores_data()
        
        # 1. 자치구 선택
        gu_list = sorted(area_df['자치구_코드_명'].dropna().unique().tolist())
        selected_gu = st.selectbox("자치구 선택", gu_list, key='selected_gu')
        
        # 2. 행정동 선택 (선택된 자치구 내)
        filtered_by_gu = area_df[area_df['자치구_코드_명'] == selected_gu]
        dong_list = sorted(filtered_by_gu['행정동_코드_명'].dropna().unique().tolist())
        selected_dong = st.selectbox("행정동 선택", dong_list, key='selected_dong')
        
        # 3. 상권 선택 (선택된 행정동 내)
        filtered_by_dong = filtered_by_gu[filtered_by_gu['행정동_코드_명'] == selected_dong]
        market_list = sorted(filtered_by_dong['상권_코드_명'].dropna().unique().tolist())
        selected_market = st.selectbox("상권 선택", market_list, key='selected_market')
        
        # 4. 업종 선택
        industry_list = sorted(stores_df['서비스_업종_코드_명'].dropna().unique().tolist())
        selected_industry = st.selectbox("업종 선택", industry_list, key='selected_industry')

        # ✅ Session state에 저장
        st.session_state['filters'] = {
            'gu': selected_gu,
            'dong': selected_dong,
            'market': selected_market,
            'industry': selected_industry
        }
        
        st.divider()

        # 빈 공간
        for _ in range(15):
            st.write("")
        
        # 로고 이미지
        img_path = os.path.join("static", "images", "logo.png")
        
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            
            st.markdown(f"""
                <div style="text-align: center; margin: 20px 0;">
                    <img src="data:image/png;base64,{data}" 
                        style="width: 300px;
                                border-radius: 15px; 
                                margin-bottom: 10px;">
                    <div style="font-size: 20px; 
                                font-weight: bold; 
                                color: #565a62;
                                margin-top: 10px;">
                        장사잘될지도
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    return choice, selected_gu, selected_dong, selected_market, selected_industry