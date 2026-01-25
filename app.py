import streamlit as st
import os
import base64
from PIL import Image
from app_home import run_home
from components.sidebar import render_sidebar
from app_overview import run_overview
from app_environment import run_environment
from app_forecast import run_forecast


def main():
    # 최대 너비 및 사이드바 배경색 스타일
    st.markdown("""
    <style>
    /* 메인 컨테이너 최대 너비 변경 */
    .block-container {
        max-width: 1200px !important;
        padding-top: 4.5rem;
        padding-bottom: 2rem;
    }
    
    /* 사이드바 배경색 */
    [data-testid="stSidebar"] {
        background-color: #e1e0df !important;
    }
    
    /* 타이틀 컨테이너 스타일 */
    .title-container {
        background:
            linear-gradient(135deg, rgba(255, 255, 255, 0.92) 0%, rgba(240, 248, 255, 0.92) 100%),
            repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(66, 133, 244, 0.03) 10px, rgba(66, 133, 244, 0.03) 20px),
            repeating-linear-gradient(-45deg, transparent, transparent 10px, rgba(52, 168, 83, 0.03) 10px, rgba(52, 168, 83, 0.03) 20px);
        background-color: #f0f8ff;
        position: relative;
        padding: 50px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        border: 2px solid rgba(66, 133, 244, 0.2);
        overflow: hidden;
    }
    .title-container::before {
        content: '🍕🍔🍿🥐🌹🚲⛽🏢';
        position: absolute;
        top: 10px;
        left: 0;
        right: 0;
        font-size: 40px;
        opacity: 0.2;
        letter-spacing: 30px;
        pointer-events: none;
    }
    .title-container::after {
        content: '♨️💈🏪🎉🎞️👔🛒👟';
        position: absolute;
        bottom: 10px;
        left: 0;
        right: 0;
        font-size: 40px;
        opacity: 0.2;
        letter-spacing: 30px;
        pointer-events: none;
    }
    .title-text {
        font-size: 52px;
        font-weight: bold;
        margin: 0;
        color: #1a73e8;
        position: relative;
        z-index: 1;
    }
    .subtitle-text {
        font-size: 20px;
        color: #5f6368;
        margin-top: 15px;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    </style>

    <div class="title-container">
        <h1 class="title-text">🗺️ 장사잘될지도</h1>
        <p class="subtitle-text">서울 상권 데이터 기반 입지 분석 & 창업 의사결정 플랫폼</p>
    </div>
""", unsafe_allow_html=True)

    # 사이드바 렌더링
    choice, selected_gu, selected_dong, selected_market, selected_industry = render_sidebar()
    # 페이지 라우팅
    if choice == '홈 화면':
        run_home() 
    elif choice == '상권 개요':
        run_overview()
    elif choice == '시장 환경':
        run_environment()
    elif choice == '상권 전망':
        run_forecast()

if __name__ == '__main__':
    main()