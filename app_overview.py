# app/app_overview.py
import streamlit as st
import pandas as pd
import numpy as np
import folium
import plotly.graph_objects as go
from streamlit_folium import st_folium
from folium import plugins
import geopandas as gpd
from shapely.geometry import shape


def run_overview():
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.title("상권 개요")
    st.markdown("""
        <hr style="
            border: none;
            border-top: 2px dashed #ccc;
            margin: 20px 0;
        ">
    """, unsafe_allow_html=True)
    st.subheader("선택한 상권의 기본 정보")
    st.markdown("""
        <div style="
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin-bottom: 30px;
        ">
            <p style="color: #495057; font-size: 15px; line-height: 1.7; margin: 0;">
                <strong>이 페이지의 핵심 질문:</strong><br>
                • 이 상권은 <span style="color: #667eea; font-weight: 600;">생활형</span>인가요, 
                <span style="color: #764ba2; font-weight: 600;">업무 중심형</span>인가요?<br>
                • <span style="color: #667eea; font-weight: 600;">언제</span> 사람이 가장 많이 몰리나요?
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.write("")
    st.write("")  

    df_area = pd.read_csv('./data/서울시_상권분석서비스_좌표변환_filtered.csv', encoding='cp949')
    df_road_population = pd.read_csv('./data/서울시 상권분석서비스(길단위인구-상권)_filtered.csv', encoding='cp949')
    df_resident_population = pd.read_csv('./data/서울시 상권분석서비스(상주인구-상권)_filtered.csv', encoding='cp949')
    df_worker_population = pd.read_csv('./data/서울시 상권분석서비스(직장인구-상권)_filtered.csv', encoding='cp949')
    df_store = pd.read_csv('./data/서울시 상권분석서비스(점포-상권)_filtered.csv', encoding='cp949')
    df_sales = pd.read_csv('./data/서울시 상권분석서비스(추정매출-상권)_filtered.csv', encoding='cp949')
    
    # ✅ Shapefile 로드
    gdf_boundary = gpd.read_file('./data/서울시_상권분석서비스_영역-상권_.shp')
    print(gdf_boundary.crs)

    # 🔁 folium용 WGS84(위·경도)로 변환
    gdf_boundary = gdf_boundary.to_crs(epsg=4326)
    
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
    selected_road_population2 = selected_road_population['총_유동인구_수'].iloc[0]
    # print(selected_road_population2)

    cond_latest_store = df_store['기준_년분기_코드'] == df_store['기준_년분기_코드'].max()
    cond_area_store   = df_store['상권_코드_명'] == selected_market
    selected_store = df_store[cond_latest_store & cond_area_store]
    selected_store = df_store[cond_latest_store & cond_area_store]
    total_store = selected_store['점포_수'].sum()
    # print(total_store)

    cond_latest_sales = df_sales['기준_년분기_코드'] == df_sales['기준_년분기_코드'].max()
    cond_area_sales   = df_sales['상권_코드_명'] == selected_market
    selected_sales = df_sales[cond_latest_sales & cond_area_sales]
    total_sales= selected_sales['당월_매출_금액'].sum()
    # print(total_sales)

    cond_latest_resident = df_resident_population['기준_년분기_코드'] == df_resident_population['기준_년분기_코드'].max()
    cond_area_resident   = df_resident_population['상권_코드_명'] == selected_market
    selected_resident_population = df_resident_population[cond_latest_resident & cond_area_resident]
    selected_resident_population = selected_resident_population['총_상주인구_수'].iloc[0]
    # print(selected_resident_population)
    
    cond_latest_worker = df_worker_population['기준_년분기_코드'] == df_worker_population['기준_년분기_코드'].max()
    cond_area_worker   = df_worker_population['상권_코드_명'] == selected_market
    selected_worker_population = df_worker_population[cond_latest_worker & cond_area_worker]
    selected_worker_population = selected_worker_population['총_직장_인구_수'].iloc[0]
    # print(selected_worker_population)
    

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
                <div class="metric-value">{format_number(selected_road_population2)}</div>
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
    st.markdown("---")
    st.write("")
    st.write("")
    st.write("")



    # ===========================
    # 🗺 Folium 지도 시각화 (경계선 추가)
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
                 선택한 상권 위치 및 경계
            </h2>
            <p style="color: rgba(255,255,255,0.9); text-align: center; margin-top: 10px; font-size: 16px;">
                 {market} | {gu} {dong}
            </p>
        </div>
    """.format(market=selected_market, gu=selected_gu, dong=selected_dong), 
    unsafe_allow_html=True)

    # ✅ 4) 선택된 상권의 경계선 추가
    # TRDAR_CD_N: 상권명 (상권_코드_명과 동일)
    selected_boundary = gdf_boundary[gdf_boundary['TRDAR_CD_N'] == selected_market]

    if not selected_boundary.empty:
        centroid = selected_boundary.geometry.centroid.iloc[0]
        center_lat, center_lon = centroid.y, centroid.x
    else:
        center_lat, center_lon = lat, lon

    # 1) 기본 지도 생성
    m = folium.Map(
        location=[center_lat, center_lon],
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

    
    
    if not selected_boundary.empty:
        # GeoJSON으로 변환하여 지도에 추가
        folium.GeoJson(
            selected_boundary.to_json(),
            name='상권 경계',
            style_function=lambda x: {
                'fillColor': '#667eea',
                'color': '#667eea',
                'weight': 3,
                'fillOpacity': 0.2,
                'dashArray': '5, 5'
            },
            highlight_function=lambda x: {
                'fillColor': '#764ba2',
                'color': '#764ba2',
                'weight': 4,
                'fillOpacity': 0.3
            },
            tooltip=folium.Tooltip(
                f"<b>{selected_market}</b><br>상권 경계",
                sticky=True
            )
        ).add_to(m)


    # 7) 미니맵 추가 (우측 하단)
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

    # 8) 전체화면 버튼
    plugins.Fullscreen(
        position='topright',
        title='전체화면',
        title_cancel='전체화면 해제',
        force_separate_button=True
    ).add_to(m)

    # 9) 레이어 컨트롤 추가
    folium.LayerControl(position='topright').add_to(m)

    # 10) Streamlit 컨테이너로 감싸기
    with st.container():
        st_folium(
            m, 
            width=None,  # 전체 너비 사용
            height=600,
            returned_objects=[]
        )

    # 경계선 정보 표시
    if not selected_boundary.empty:
        # 1) 면적 계산용으로 다시 투영 좌표계(5181)로 변환
        boundary_for_area = selected_boundary.to_crs(epsg=5181)

        # 2) m² → km²
        area_km2 = boundary_for_area.geometry.area.iloc[0] / 1_000_000

        st.info(f"📍 **상권 면적**: 약 {area_km2:.3f} km²")

    st.write("")
    st.write("")
    st.write("")
    st.markdown("---")
    st.write("")
    st.write("")
    st.write("")

    # 인구 구성 비교 차트
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <h2 style="color: white; margin: 0; text-align: center;">
                인구 구성
            </h2>
            <p style="color: rgba(255,255,255,0.9); text-align: center; margin-top: 10px; font-size: 16px;">
                상주 인구 vs 직장 인구 Bar Chart
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 데이터 준비
    population_data = pd.DataFrame({
        '구분': ['상주 인구', '직장 인구'],
        '인구수': [selected_resident_population, selected_worker_population]
    })
    
    fig = go.Figure()

    # 막대 그래프 추가
    fig.add_trace(go.Bar(
        x=population_data['구분'],
        y=population_data['인구수'],
        text=[format_number(x) for x in population_data['인구수']],
        textposition='auto',
        width=0.3,
        marker=dict(
            color=['#667eea', '#764ba2'],
            line=dict(color='white', width=2)
        ),
        hovertemplate='<b>%{x}</b><br>인구수: %{y:,}명<extra></extra>'
    ))

    # 레이아웃 설정
    fig.update_layout(
        title={
            'text': '상주 인구 vs 직장 인구',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#1a1a1a', 'family': 'Arial'}
        },
        xaxis=dict(
            title=dict(
                text='구분',
                font=dict(size=14, color='#666')
            ),
            tickfont=dict(size=12, color='#1a1a1a')
        ),
        yaxis=dict(
            title=dict(
                text='인구 수 (명)',
                font=dict(size=14, color='#666')
            ),
            tickfont=dict(size=12, color='#1a1a1a'),
            gridcolor='#f0f0f0'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)

    # 간단한 분석 텍스트
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🏠 상주 인구</div>
                <div class="metric-value">{format_number(selected_resident_population)}명</div>
                <p style="color: #888; font-size: 12px; margin-top: 10px;">
                    해당 지역에 실제 거주하는 인구
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">💼 직장 인구</div>
                <div class="metric-value">{format_number(selected_worker_population)}명</div>
                <p style="color: #888; font-size: 12px; margin-top: 10px;">
                    해당 지역에서 근무하는 인구
                </p>
            </div>
        """, unsafe_allow_html=True)

    # 안내 멘트 추가
    st.markdown("""
        <div style="
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 12px 16px;
            border-radius: 6px;
            margin-top: 20px;
        ">
            <p style="color: #856404; font-size: 13px; margin: 0; line-height: 1.6;">
                ℹ️ <strong>안내:</strong> 표시되는 상권은 행정동과 범위가 달라, 인구가 작게 보이더라도 실제 이용 규모와는 차이가 있을 수 있습니다.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.write("")
    st.markdown("---")
    st.write("")
    st.write("")
    st.write("")


    # 시간대별 유동인구 라인차트
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <h2 style="color: white; margin: 0; text-align: center;">
                 시간대별 유동인구 변화
            </h2>
            <p style="color: rgba(255,255,255,0.9); text-align: center; margin-top: 10px; font-size: 16px;">
                하루 시간대별 유동인구 추이
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 시간대별 데이터 추출 (selected_road_population에서 직접)
    flow_row = selected_road_population.iloc[0]

    # 시간대별 데이터 준비
    time_data = pd.DataFrame({
        '시간대': ['00-06시', '06-11시', '11-14시', '14-17시', '17-21시', '21-24시'],
        '유동인구': [
            flow_row['시간대_00_06_유동인구_수'],
            flow_row['시간대_06_11_유동인구_수'],
            flow_row['시간대_11_14_유동인구_수'],
            flow_row['시간대_14_17_유동인구_수'],
            flow_row['시간대_17_21_유동인구_수'],
            flow_row['시간대_21_24_유동인구_수']
        ]
    })

    # 라인 차트 생성
    fig_time = go.Figure()

    fig_time.add_trace(go.Scatter(
        x=time_data['시간대'],
        y=time_data['유동인구'],
        mode='lines+markers',
        line=dict(color='#667eea', width=3),
        marker=dict(size=10, color='#764ba2', line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.1)',
        hovertemplate='<b>%{x}</b><br>유동인구: %{y:,}명<extra></extra>'
    ))

    fig_time.update_layout(
        title={
            'text': '하루 시간대별 유동인구 추이',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#1a1a1a', 'family': 'Arial'}
        },
        xaxis=dict(
            title=dict(
                text='시간대',
                font=dict(size=14, color='#666')
            ),
            tickfont=dict(size=12, color='#1a1a1a')
        ),
        yaxis=dict(
            title=dict(
                text='유동인구 (명)',
                font=dict(size=14, color='#666')
            ),
            tickfont=dict(size=12, color='#1a1a1a'),
            gridcolor='#f0f0f0'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        hovermode='x unified'
    )

    st.plotly_chart(fig_time, use_container_width=True)

    # 피크 시간대 분석
    peak_time = time_data.loc[time_data['유동인구'].idxmax()]
    low_time = time_data.loc[time_data['유동인구'].idxmin()]

    col1, col2 = st.columns(2)
    with col1:
        st.success(f" **피크 시간대**: {peak_time['시간대']} ({format_number(peak_time['유동인구'])}명)")
    with col2:
        st.info(f" **최저 시간대**: {low_time['시간대']} ({format_number(low_time['유동인구'])}명)")


    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
