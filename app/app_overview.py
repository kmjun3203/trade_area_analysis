# app/app_overview.py
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium import plugins


def run_overview():
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    df_area = pd.read_csv('../data/서울시_상권분석서비스_좌표변환.csv')
    df_road_population = pd.read_csv('../data/서울시 상권분석서비스(길단위인구-상권).csv', encoding='cp949')
    df_resident_population = pd.read_csv('../data/서울시 상권분석서비스(상주인구-상권).csv', encoding='cp949')
    df_worker_population = pd.read_csv('../data/서울시 상권분석서비스(직장인구-상권).csv', encoding='cp949')
    df_store = pd.read_csv('../data/서울시 상권분석서비스(점포-상권).csv', encoding='cp949')
    df_sales = pd.read_csv('../data/서울시 상권분석서비스(추정매출-상권).csv', encoding='cp949')

    # ✅ Session state에서 필터 정보 가져오기
    filters = st.session_state.get('filters', {})
    
    selected_gu = filters.get('gu')
    selected_dong = filters.get('dong')
    selected_market = filters.get('market')
    selected_industry = filters.get('industry')

    # ✅ 선택된 상권의 위도/경도 추출
    lat, lon = df_area.loc[
        df_area['상권_코드_명'] == selected_market,
        ['위도', '경도']
    ].iloc[0]

    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <h2 style="color: white; margin: 0; text-align: center;">
                 선택한 상권 정보
            </h2>
            <p style="color: rgba(255,255,255,0.9); text-align: center; margin-top: 10px; font-size: 16px;">
                 {market} | {gu} {dong}
            </p>
        </div>
    """.format(market=selected_market, gu=selected_gu, dong=selected_dong), 
    unsafe_allow_html=True)

    cond_latest = df_road_population['기준_년분기_코드'] == df_road_population['기준_년분기_코드'].max()
    cond_area   = df_road_population['상권_코드_명'] == selected_market
    selected_road_population = df_road_population[cond_latest & cond_area]
    selected_road_population = selected_road_population['총_유동인구_수'].iloc[0]
    print(selected_road_population)

    cond_latest_store = df_store['기준_년분기_코드'] == df_store['기준_년분기_코드'].max()
    cond_area_store   = df_store['상권_코드_명'] == selected_market
    selected_store = df_store[cond_latest_store & cond_area_store]
    selected_store = df_store[cond_latest_store & cond_area_store]
    total_store = selected_store['점포_수'].sum()
    print(total_store)

    cond_latest_sales = df_sales['기준_년분기_코드'] == df_sales['기준_년분기_코드'].max()
    cond_area_sales   = df_sales['상권_코드_명'] == selected_market
    selected_sales = df_sales[cond_latest_sales & cond_area_sales]
    total_sales= selected_sales['당월_매출_금액'].sum()
    print(total_sales)

    def format_number(num):
        if num >= 100000000:  # 1억 이상
            return f"{num/100000000:.1f}억"
        elif num >= 10000:  # 1만 이상
            return f"{num/10000:.1f}만"
        else:
            return f"{num:,.0f}"
        
    st.markdown("""
    <style>
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
        text-align: center;
        height: 100%;
    }
    .metric-label {
        color: #666;
        font-size: 14px;
        margin-bottom: 10px;
        font-weight: 500;
    }
    .metric-value {
        color: #1a1a1a;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🚶 유동 인구 수</div>
                <div class="metric-value">{format_number(selected_road_population)}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🏪 점포 수</div>
                <div class="metric-value">{format_number(total_store)}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">💰 추정 총 매출</div>
                <div class="metric-value">{format_number(total_sales)}원</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")


    # ===========================
    # 🗺 Folium 지도 시각화 (개선)
    # ===========================

    # 헤더 영역 - 예쁜 배경과 아이콘
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <h2 style="color: white; margin: 0; text-align: center;">
                 선택한 상권 위치
            </h2>
            <p style="color: rgba(255,255,255,0.9); text-align: center; margin-top: 10px; font-size: 16px;">
                 {market} | {gu} {dong}
            </p>
        </div>
    """.format(market=selected_market, gu=selected_gu, dong=selected_dong), 
    unsafe_allow_html=True)

    # 1) 기본 지도 생성
    m = folium.Map(
        location=[lat, lon],
        zoom_start=16,
        tiles=None,  # 커스텀 타일 사용
        control_scale=True,  # 축척 표시
    )

    # 2) 예쁜 타일 레이어 추가
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        name='Light Map',
        overlay=False,
        control=True
    ).add_to(m)

    # 3) 위성 타일 레이어 (선택 가능)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(m)

    # 4) 선택 상권 중심 원형 마커 (펄스 효과)
    folium.CircleMarker(
        location=[lat, lon],
        radius=15,
        color="#667eea",
        weight=4,
        fill=True,
        fill_color="#764ba2",
        fill_opacity=0.7,
        popup=folium.Popup(
            f"""
            <div style="font-family: Arial; width: 200px;">
                <h4 style="color: #667eea; margin-bottom: 10px;">🎯 {selected_market}</h4>
                <hr style="margin: 10px 0;">
                <p style="margin: 5px 0;"><b>자치구:</b> {selected_gu}</p>
                <p style="margin: 5px 0;"><b>행정동:</b> {selected_dong}</p>
                <p style="margin: 5px 0;"><b>업종:</b> {selected_industry}</p>
            </div>
            """,
            max_width=250
        ),
        tooltip=f"<b>{selected_market}</b><br>클릭하면 상세정보를 볼 수 있습니다",
    ).add_to(m)

    # 5) 중심점 정확한 위치 표시 (작은 점)
    folium.Circle(
        location=[lat, lon],
        radius=50,  # 미터 단위
        color="#ff6b6b",
        fill=True,
        fill_color="#ff6b6b",
        fill_opacity=0.3,
        weight=2,
    ).add_to(m)

    # 6) 미니맵 추가 (우측 하단)
    minimap = plugins.MiniMap(
        tile_layer='OpenStreetMap',
        position='bottomright',
        width=150,
        height=150,
        collapsed_width=25,
        collapsed_height=25,
        zoom_level_offset=-5
    )
    m.add_child(minimap)

    # 7) 전체화면 버튼
    plugins.Fullscreen(
        position='topright',
        title='전체화면',
        title_cancel='전체화면 해제',
        force_separate_button=True
    ).add_to(m)

    # 8) 레이어 컨트롤 추가
    folium.LayerControl(position='topright').add_to(m)

    # 9) Streamlit 컨테이너로 감싸기
    with st.container():
        st_folium(
            m, 
            width=None,  # 전체 너비 사용
            height=600,
            returned_objects=[]
        )

   

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
