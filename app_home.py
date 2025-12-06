import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from koreanize_matplotlib import koreanize
import plotly.express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster    
koreanize()

def run_home():
    df_area = pd.read_csv("./data/서울시_상권분석서비스_좌표변환.csv")
    df_area['행정동_코드_명'] = df_area['행정동_코드_명'].str.replace('?', '·')
    df_area['상권_코드_명'] = df_area['상권_코드_명'].str.replace('?', '·')

    # ===== 홈 화면: 서울시 전체 개요 =====
    st.header("📊 서울시 상권 현황")

    # 최상단 핵심 지표
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("총 상권 수", f"{len(df_area):,}개")
    with col2:
        st.metric("행정동 수", f"{df_area['행정동_코드_명'].nunique()}개")
    with col3:
        st.metric("자치구 수", f"{df_area['자치구_코드_명'].nunique()}개")
    with col4:
        st.metric("총 상권 면적", f"{df_area['영역_면적'].sum()/1000000:.1f}km²")

    st.divider()

    # 상권 구분 현황
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📊 상권 구분별 현황")
        type_stats = df_area.groupby('상권_구분_코드_명').agg({
            '상권_코드_명': 'count',
            '영역_면적': 'sum'
        }).reset_index()
        type_stats.columns = ['상권구분', '상권수', '총면적(㎡)']
        type_stats['총면적(㎡)'] = type_stats['총면적(㎡)'].apply(lambda x: f"{x:,}")
        st.dataframe(type_stats, use_container_width=True)

    with col2:
        st.subheader("🥧 상권 구분 비율")
        fig = px.pie(df_area, names='상권_구분_코드_명',
                     title='상권 구분별 비율',
                     hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # 자치구별 TOP 10
    st.subheader("🏆 자치구별 상권 수 TOP 10")
    gu_count = df_area['자치구_코드_명'].value_counts().head(10).reset_index()
    gu_count.columns = ['자치구', '상권수']

    fig = px.bar(gu_count, x='자치구', y='상권수',
                 color='상권수',
                 color_continuous_scale='Blues',
                 text='상권수')
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ===== 행정동별 지도 및 상세 분석 =====
    st.header("🗺️ 행정동별 상권 분석")

    # 행정동별 상권 수 및 중심좌표 계산
    dong_summary = df_area.groupby('행정동_코드_명').agg({
        '상권_코드_명': 'count',
        '위도': 'mean',
        '경도': 'mean',
        '영역_면적': 'sum',
        '자치구_코드_명': 'first'
    }).reset_index()
    dong_summary.columns = ['행정동', '상권수', '위도', '경도', '총면적', '자치구']


    # 행정동 선택
    choice_dong = st.selectbox('📍 행정동을 선택하세요', sorted(df_area['행정동_코드_명'].unique()))

    # 선택된 행정동 필터링
    filtered_df = df_area[df_area['행정동_코드_명'] == choice_dong]
    dong_type_count = filtered_df['상권_구분_코드_명'].value_counts().reset_index()
    dong_type_count.columns = ['상권구분', '개수']

    # === 기본 정보 ===
    st.write(f"### {choice_dong} 기본 정보")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("총 상권 수", len(filtered_df))
    with col2:
        st.metric("총 영역 면적", f"{filtered_df['영역_면적'].sum():,}㎡")
    with col3:
        st.metric("평균 상권 면적", f"{filtered_df['영역_면적'].mean():,.0f}㎡")

    st.divider()

    # === 상권구분 정보 ===
    col1, col2 = st.columns([1, 2])

    with col1:
        st.write("#### 상권구분별 개수")
        st.dataframe(dong_type_count, use_container_width=True)

    with col2:
        fig = px.pie(dong_type_count, values='개수', names='상권구분',
                    title=f'{choice_dong} 상권구분 비율',
                    hole=0.3)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # === 선택된 행정동의 상권 지도 ===
    st.write(f"#### 🗺️ {choice_dong} 상권 위치")

    center_lat = filtered_df['위도'].mean()
    center_lon = filtered_df['경도'].mean()

    detail_map = folium.Map(location=[center_lat, center_lon], zoom_start=14)

    # 색상 매핑
    color_map = {
        '골목상권': 'blue',
        '발달상권': 'red',
        '전통시장': 'green',
        '관광특구': 'purple'
    }

    # 상권별 마커 추가
    for idx, row in filtered_df.iterrows():
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=f"{row['상권_코드_명']}<br>{row['상권_구분_코드_명']}<br>{row['영역_면적']:,}㎡",
            tooltip=row['상권_코드_명'],
            icon=folium.Icon(color=color_map.get(row['상권_구분_코드_명'], 'gray'))
        ).add_to(detail_map)

    st_folium(detail_map, width=None, height=500, key="detail_map")

    st.divider()

    # === 상권 상세 정보 ===
    st.write(f"#### 📍 {choice_dong} 상권 목록")
    display_df = filtered_df[['상권_코드_명', '상권_구분_코드_명', '영역_면적', '자치구_코드_명']].copy()
    display_df['영역_면적'] = display_df['영역_면적'].apply(lambda x: f"{x:,}㎡")
    st.dataframe(display_df, use_container_width=True)

    # === 면적 순위 ===
    st.write("#### 📊 면적 순위")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**가장 큰 상권 TOP 5**")
        largest = filtered_df.nlargest(5, '영역_면적')[['상권_코드_명', '영역_면적']].copy()
        largest['영역_면적'] = largest['영역_면적'].apply(lambda x: f"{x:,}㎡")
        st.dataframe(largest, use_container_width=True)

    with col2:
        st.write("**가장 작은 상권 TOP 5**")
        smallest = filtered_df.nsmallest(5, '영역_면적')[['상권_코드_명', '영역_면적']].copy()
        smallest['영역_면적'] = smallest['영역_면적'].apply(lambda x: f"{x:,}㎡")
        st.dataframe(smallest, use_container_width=True)

    st.divider()

    # === 서울 전체와 비교 ===
    st.write("#### 🔍 서울 전체와 비교")
    col1, col2, col3 = st.columns(3)

    avg_count_per_dong = len(df_area) / df_area['행정동_코드_명'].nunique()
    seoul_avg_area = df_area['영역_면적'].mean()
    this_dong_avg_area = filtered_df['영역_면적'].mean()

    with col1:
        st.metric("이 행정동 상권 수",
                len(filtered_df),
                delta=f"{len(filtered_df) - avg_count_per_dong:.1f}",
                delta_color="normal")

    with col2:
        st.metric("서울 평균 상권 수",
                f"{avg_count_per_dong:.1f}")

    with col3:
        st.metric("이 행정동 평균 면적",
                f"{this_dong_avg_area:,.0f}㎡",
                delta=f"{this_dong_avg_area - seoul_avg_area:,.0f}㎡",
                delta_color="normal")

    st.divider()

    # === 서울시 전체 행정동 비교 ===
    st.write("#### 🏙️ 서울시 전체 행정동 비교")

    dong_comparison = df_area.groupby('행정동_코드_명').agg({
        '상권_코드_명': 'count',
        '영역_면적': 'sum',
        '자치구_코드_명': 'first'
    }).reset_index()
    dong_comparison.columns = ['행정동', '상권수', '총면적(㎡)', '자치구']
    dong_comparison = dong_comparison.sort_values('상권수', ascending=False).reset_index(drop=True)

    # 현재 선택된 행정동 순위 (정렬 후 인덱스 기반)
    rank = dong_comparison[dong_comparison['행정동'] == choice_dong].index[0] + 1
    total_dongs = len(dong_comparison)

    # 면적 포맷팅 (순위 계산 후)
    dong_comparison['총면적(㎡)'] = dong_comparison['총면적(㎡)'].apply(lambda x: f"{x:,}")

    st.info(f"📍 **{choice_dong}**은 서울시 전체 {total_dongs}개 행정동 중 **{rank}위**입니다.")

    st.dataframe(dong_comparison, use_container_width=True)




