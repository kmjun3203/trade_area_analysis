import os
import streamlit as st
import plotly.express as px
import pandas as pd
from koreanize_matplotlib import koreanize


koreanize()

def run_detail():
    df_area = pd.read_csv("./data/서울시_상권분석서비스_좌표변환.csv")
    df_area['행정동_코드_명'] = df_area['행정동_코드_명'].str.replace('?', '·')
    df_area['상권_코드_명'] = df_area['상권_코드_명'].str.replace('?', '·')



    # 초기화 버튼
    if st.button("🔄 선택 초기화", key="reset_btn"):
        st.rerun()

    # 색상 매핑
    color_map = {
        '골목상권': '#1f77b4',
        '발달상권': '#ff7f0e', 
        '전통시장': '#2ca02c',
        '관광특구': '#9467bd'
    }

    # 지도 생성
    fig = px.scatter_mapbox(
        df_area,
        lat='위도',
        lon='경도',
        hover_name='상권_코드_명',
        hover_data={
            '상권_구분_코드_명': True,
            '자치구_코드_명': True,
            '행정동_코드_명': True,
            '영역_면적': ':,',
            '위도': ':.6f',
            '경도': ':.6f'
        },
        color='상권_구분_코드_명',
        color_discrete_map=color_map,
        zoom=10,
        height=600,
        mapbox_style="open-street-map"
    )

    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    # 클릭 이벤트
    event = st.plotly_chart(fig, use_container_width=True, 
                            on_select="rerun",
                            key="sangwon_map")

    # 클릭한 상권 정보 표시
    if event and event.selection and event.selection.points:
        idx = event.selection.points[0]['point_index']
        selected = df_area.iloc[idx]
        
        st.divider()
        st.success(f"✅ **{selected['상권_코드_명']}**")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("상권구분", selected['상권_구분_코드_명'])
        with col2:
            st.metric("자치구", selected['자치구_코드_명'])
        with col3:
            st.metric("행정동", selected['행정동_코드_명'])
        with col4:
            st.metric("면적", f"{selected['영역_면적']:,}㎡")