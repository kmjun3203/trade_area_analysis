import streamlit as st
from app_home import run_home

def main():
    # 커스텀 CSS 스타일
    st.markdown("""
        <style>
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
            content: '🏢 🏪 🏬 🏛️ 🏗️ 🌆 🗺️ 📍 🧭 🌐';
            position: absolute;
            top: 10px;
            left: 0;
            right: 0;
            font-size: 40px;
            opacity: 0.08;
            letter-spacing: 30px;
            pointer-events: none;
        }
        .title-container::after {
            content: '📊 📈 💼 🏙️ 🗾 🎯 💡 🔍 📌 ⭐';
            position: absolute;
            bottom: 10px;
            left: 0;
            right: 0;
            font-size: 40px;
            opacity: 0.08;
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
            <h1 class="title-text"> 장사잘될지도</h1>
            <p class="subtitle-text">서울 상권 데이터 기반 입지 분석 플랫폼</p>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.title("기능")
    menu = ['홈 화면', '상권 상세 분석', 'AI예측']


    choice = st.sidebar.selectbox('메뉴', menu)

    if choice == menu[0]:
        run_home() 
    elif choice == menu[1]:
        pass
        # from app_detail import run_detail
        # run_detail()
    elif choice == menu[2]:
        pass
        # from app_ai import run_ai
        # run_ai()


if __name__ == '__main__':
    main()