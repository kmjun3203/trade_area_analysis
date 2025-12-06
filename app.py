import streamlit as st
import os
import base64
from app_home import run_home
from app_detail import run_detail
from PIL import Image

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
            background: linear-gradient(135deg, #1a73e8 0%, #34a853 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
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
            <h1 class="title-text"><span style="filter: none; -webkit-text-fill-color: initial;">🗺️</span>장사잘될지도</h1>
            <p class="subtitle-text">서울 상권 데이터 기반 입지 분석 플랫폼</p>
        </div>
    """, unsafe_allow_html=True)

    # 사이드바
    with st.sidebar:
        st.title("Menu")
        menu = ['홈 화면', '상권 상세 분석', 'AI예측']
        choice = st.selectbox('선택', menu)
        
        st.divider()

        # 빈 공간 추가 (이미지를 더 아래로)
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
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
   

        
        
        # 이미지를 셀렉트박스 아래로 이동
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

    if choice == menu[0]:
        run_home() 
    elif choice == menu[1]:
        run_detail()
    elif choice == menu[2]:
        pass


if __name__ == '__main__':
    main()