import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import plotly.graph_objects as go

def calc_competition_level(
    df_store: pd.DataFrame, df_area: pd.DataFrame, selected_market: str, selected_industry: str,latest_quarter: int
    ) -> dict:
        """
        이미 필터링된 데이터로 경쟁 강도만 계산
        """
        
        # 1) 선택 상권의 면적 가져오기
        area_row = df_area[df_area['상권_코드_명'] == selected_market]
        if area_row.empty:
            return None
        
        area_m2 = float(area_row['영역_면적'].median())
        area_km2 = area_m2 / 1_000_000.0
        
        # 2) 선택 상권의 해당 업종 점포 수
        cond_latest = df_store['기준_년분기_코드'] == latest_quarter
        cond_area = df_store['상권_코드_명'] == selected_market
        cond_industry = df_store['서비스_업종_코드_명'] == selected_industry
        
        stores = df_store[cond_latest & cond_area & cond_industry]['점포_수'].sum()
        
        # 3) 점포 밀도 계산
        density_per_km2 = stores / area_km2 if area_km2 > 0 else 0
        
        # 4) 서울 전체 상권의 동일 업종 밀도 분포로 등급 계산
        # 상권별 면적 테이블
        area_by_code = (
            df_area.groupby('상권_코드', as_index=False)['영역_면적']
            .median()
            .rename(columns={'영역_면적': 'area_m2'})
        )
        
        # 최신 분기, 해당 업종만
        base = df_store[(df_store['기준_년분기_코드'] == latest_quarter) & 
                        (df_store['서비스_업종_코드_명'] == selected_industry)].copy()
        
        # 면적 조인
        base = base.merge(area_by_code, on='상권_코드', how='left')
        base = base[base['area_m2'].notna() & (base['area_m2'] > 0)].copy()
        base['area_km2'] = base['area_m2'] / 1_000_000.0
        
        # 상권별 점포 밀도 계산
        market_stores = base.groupby('상권_코드', as_index=False)['점포_수'].sum()
        market_area = base.groupby('상권_코드', as_index=False)['area_km2'].median()
        dist = market_stores.merge(market_area, on='상권_코드', how='inner')
        dist['density'] = dist['점포_수'] / dist['area_km2']
        
        # 분위수로 등급 결정 (33%/66%)
        if dist.empty or dist['density'].notna().sum() < 10:
            level = "판단불가"
            thresholds = {}
        else:
            q33, q66 = dist['density'].quantile([0.33, 0.66]).tolist()
            
            if density_per_km2 < q33:
                level = "낮음"
            elif density_per_km2 < q66:
                level = "보통"
            else:
                level = "높음"
            
            thresholds = {"low_cut": float(q33), "high_cut": float(q66)}
        
        return {
            "area_km2": area_km2,
            "stores": int(stores),
            "density_per_km2": density_per_km2,
            "level": level,
            "thresholds": thresholds
        }

def run_environment():

    filters = st.session_state.get('filters', {})

    selected_gu = filters.get('gu')
    selected_dong = filters.get('dong')
    selected_market = filters.get('market')
    selected_industry = filters.get('industry')

    # print(selected_industry)

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.title("시장 환경")
    st.markdown("""
        <hr style="
            border: none;
            border-top: 2px dashed #ccc;
            margin: 20px 0;
        ">
    """, unsafe_allow_html=True)
    st.subheader("시장 경쟁 환경 분석")
    st.markdown("""
        <div style="
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin-bottom: 30px;
        ">
            <p style="color: #495057; font-size: 15px; line-height: 1.7; margin: 0;">
                💡 <strong>이 페이지의 핵심 질문:</strong><br>
                • 특정 업종이 <span style="color: #667eea; font-weight: 600;">과도하게 몰려 있는지</span><br>
                • 시장이 이미 <span style="color: #764ba2; font-weight: 600;">포화 상태</span>인지<br>
                • 소비 여력이 <span style="color: #667eea; font-weight: 600;">받쳐주는지</span>
            </p>
            <hr style="border: none; border-top: 1px solid #dee2e6; margin: 15px 0;">
            <p style="color: #495057; font-size: 20px; line-height: 1.7; margin: 0;">
                <strong>선택 업종 현황</strong><br>
                <span style="color: #667eea; font-weight: 600;">{industry}</span>
            </p>
        </div>
    """.format(industry=selected_industry), unsafe_allow_html=True)


    font_path = "C:/Windows/Fonts/malgun.ttf"  # 윈도우
    font = fm.FontProperties(fname=font_path)
    plt.rcParams["font.family"] = font.get_name()
    plt.rcParams["axes.unicode_minus"] = False

    df_store = pd.read_csv('./data/서울시 상권분석서비스(점포-상권)_filtered.csv', encoding='cp949')
    df_sales = pd.read_csv('./data/서울시 상권분석서비스(추정매출-상권)_filtered.csv', encoding='cp949')
    df_facilities = pd.read_csv('./data/서울시 상권분석서비스(집객시설-상권)_filtered.csv', encoding='cp949')
    df_income = pd.read_csv('./data/서울시 상권분석서비스(소득소비-상권)_filtered.csv', encoding='cp949')
    df_area = pd.read_csv('./data/서울시 상권분석서비스(영역-상권)_filtered.csv', encoding='cp949')

    latest_quarter = df_store['기준_년분기_코드'].max()

    cond_latest = df_store['기준_년분기_코드'] == df_store['기준_년분기_코드'].max()
    cond_area   = df_store['상권_코드_명'] == selected_market
    selected_store_df = df_store[cond_latest & cond_area]
    grouped_selected_store_df = (selected_store_df.groupby('서비스_업종_코드_명')['점포_수'].sum().sort_values(ascending=False))
    # print(grouped_selected_store_df)

    cond_latest_income = df_income['기준_년분기_코드'] == df_income['기준_년분기_코드'].max()
    cond_area_income = df_income['상권_코드_명'] == selected_market
    selected_income_df = df_income[cond_latest_income & cond_area_income]
    print(selected_income_df)
    value_income = selected_income_df['지출_총금액'].iloc[0] if not selected_income_df.empty else 0

    # 필터링
    filtered_sales = df_sales.loc[
        (df_sales['기준_년분기_코드'] == df_sales['기준_년분기_코드'].max()) &
        (df_sales['서비스_업종_코드_명'] == selected_industry) &
        (df_sales['상권_코드_명'] == selected_market),
        '당월_매출_금액'
    ]

    # 안전하게 값 가져오기
    # 업종별 추정 매출 금액
    value = filtered_sales.iloc[0] if not filtered_sales.empty else 0
    print(value)

    # 수치 포맷팅 함수
    def format_number(num):
        if num >= 100000000:  # 1억 이상
            return f"{num/100000000:.1f}억"
        elif num >= 10000:  # 1만 이상
            return f"{num/10000:.1f}만"
        else:
            return f"{num:,.0f}"

    if value > 0:
        st.markdown(f"""
            <div style="
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            ">
                <p style="color: #495057; font-size: 15px; line-height: 1.7; margin: 0;">
                    <strong style="color: #1a1a1a; font-size: 20px;">추정매출</strong>
                </p>
                <p style="color: #495057; font-size: 15px; line-height: 1.7; margin: 0;">
                    <strong style="color: #667eea;">{selected_market}</strong> 상권에서 
                    <strong style="color: #764ba2;">{selected_industry}</strong> 업종의 추정 매출은 
                    <strong style="color: #1a1a1a; font-size: 20px;">{format_number(value)}원</strong>입니다.
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            ">
                <p style="color: #495057; font-size: 15px; line-height: 1.7; margin: 0;">
                    <strong style="color: #667eea;">{selected_market}</strong> 상권에서 
                    <strong style="color: #764ba2;">{selected_industry}</strong> 업종의 매출 데이터가 없습니다.
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
    st.markdown("---")

    # 상위 10개 업종 차트
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <h2 style="color: white; margin: 0; text-align: center;">
                업종별 점포 수 분석
            </h2>
            <p style="color: rgba(255,255,255,0.9); text-align: center; margin-top: 10px; font-size: 16px;">
                상위 10개 업종 집중도
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 상위 10개 데이터 추출
    top_10_stores = grouped_selected_store_df.head(10)
    
    # 선택한 업종이 상위 10개에 있는지 확인
    selected_industry_rank = None
    if selected_industry in top_10_stores.index:
        selected_industry_rank = list(top_10_stores.index).index(selected_industry) + 1
    
    # 색상 설정 (선택 업종 강조)
    colors = ['#667eea' if idx == selected_industry else '#764ba2' 
              for idx in top_10_stores.index]
    
    # Plotly 바 차트 생성
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=top_10_stores.index,
        x=top_10_stores.values,
        orientation='h',
        text=top_10_stores.values,
        textposition='auto',
        marker=dict(
            color=colors,
            line=dict(color='white', width=2)
        ),
        hovertemplate='<b>%{y}</b><br>점포 수: %{x}개<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': '상위 10개 업종별 점포 수',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#1a1a1a', 'family': 'Arial'}
        },
        xaxis=dict(
            title=dict(
                text='점포 수 (개)',
                font=dict(size=14, color='#666')
            ),
            tickfont=dict(size=12, color='#1a1a1a'),
            gridcolor='#f0f0f0'
        ),
        yaxis=dict(
            title=dict(
                text='업종',
                font=dict(size=14, color='#666')
            ),
            tickfont=dict(size=12, color='#1a1a1a'),
            autorange='reversed'  # 상위부터 표시
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        margin=dict(l=150, r=50, t=80, b=50),
        hovermode='y unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 분석 정보
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🥇 1위 업종",
            value=top_10_stores.index[0],
            delta=f"{top_10_stores.values[0]}개"
        )
    
    with col2:
        st.metric(
            label="전체 업종 수",
            value=f"{len(grouped_selected_store_df)}개"
        )
    
    with col3:
        if selected_industry_rank:
            st.metric(
                label="선택 업종 순위",
                value=f"{selected_industry_rank}위",
                delta=f"{top_10_stores[selected_industry]}개"
            )
        else:
            st.metric(
                label="선택 업종 순위",
                value="10위 밖",
                delta="상위권 아님"
            )
    


    # 전체 업종 테이블
    

    # DataFrame으로 변환
    all_stores_df = pd.DataFrame({
        '순위': range(1, len(grouped_selected_store_df) + 1),
        '업종명': grouped_selected_store_df.index,
        '점포 수': grouped_selected_store_df.values
    })

    # 선택 업종 하이라이트를 위한 스타일링
    def highlight_selected(row):
        if row['업종명'] == selected_industry:
            return ['background-color: #e8eaf6; font-weight: bold'] * len(row)
        else:
            return [''] * len(row)

    # 테이블 표시
    st.dataframe(
        all_stores_df.style.apply(highlight_selected, axis=1),
        use_container_width=True,
        height=400
    )
    
    
    competition_result = calc_competition_level(
        df_store=df_store,
        df_area=df_area,
        selected_market=selected_market,
        selected_industry=selected_industry,
        latest_quarter=latest_quarter
    )
    st.write("")
    st.write("")
    st.write("")
    st.markdown("---")
    st.write("")
    st.write("")
    st.write("")
    if competition_result:
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                <h2 style="color: white; margin: 0; text-align: center;">
                    선택한 업종의 경쟁 강도
                </h2>
                <p style="color: rgba(255,255,255,0.9); text-align: center; margin-top: 10px; font-size: 16px;">
                    점포 밀도 지표
                </p>
                <p style="color: rgba(255,255,255,0.9); text-align: center; margin-top: 10px; font-size: 16px;">
                    경쟁 강도 (낮음 / 보통 / 높음)
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="상권 면적",
                value=f"{competition_result['area_km2']:.2f} km²"
            )
        
        with col2:
            st.metric(
                label="점포 수",
                value=f"{competition_result['stores']}개"
            )
        
        with col3:
            st.metric(
                label="점포 밀도",
                value=f"{competition_result['density_per_km2']:.1f}개/km²"
            )
        
        with col4:
            level = competition_result['level']
            if level == "높음":
                st.metric(
                    label="경쟁 강도",
                    value=level,
                    delta="치열함",
                    delta_color="inverse"
                )
            elif level == "보통":
                st.metric(
                    label="경쟁 강도",
                    value=level,
                    delta="적정함"
                )
            else:
                st.metric(
                    label="경쟁 강도",
                    value=level,
                    delta="여유있음",
                    delta_color="normal"
                )

        st.write("")
        st.write("")

            # 점포 밀도 설명
        st.markdown("""
            <div style="
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #667eea;
                margin-bottom: 20px;
            ">
                <p style="color: #495057; font-size: 15px; line-height: 1.8; margin: 0;">
                    <strong style="color: #667eea;">📊 점포 밀도란?</strong><br>
                    점포 밀도는 상권 면적 대비 점포 수를 의미합니다. 
                    해당 상권은 약 <span style="font-weight: 600;">{area_m2:,.0f}㎡</span> 면적에 
                    <span style="font-weight: 600;">{stores}개</span>의 점포가 분포해 있습니다.<br>
                     “만약 이 상권과 같은 점포 분포가 1km² 크기까지 넓어진다면 점포가 몇 개 있을까?”에 대한 값은 <span style="font-weight: 600;">{density:.1f}개/km²</span>입니다.
                </p>
            </div>
        """.format(
            area_m2=competition_result['area_km2'] * 1_000_000,
            stores=competition_result['stores'],
            density=competition_result['density_per_km2']
        ), unsafe_allow_html=True)
        
        # 경쟁 강도 설명
        st.markdown("""
            <div style="
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #764ba2;
                margin-bottom: 20px;
            ">
                <p style="color: #495057; font-size: 15px; line-height: 1.8; margin: 0;">
                    <strong style="color: #764ba2;">🎯 경쟁 강도란?</strong><br>
                    경쟁 강도는 상권 면적 대비 점포 밀도를 기준으로 산정합니다. 
                    동일 업종의 점포 밀도를 서울 전체 상권과 비교하여 
                    상대적으로 <span style="font-weight: 600; color: #28a745;">낮음</span> / 
                    <span style="font-weight: 600; color: #ffc107;">보통</span> / 
                    <span style="font-weight: 600; color: #dc3545;">높음</span>으로 분류합니다.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if level == "높음":
            st.warning(f"**{selected_industry}** 업종의 경쟁 강도가 **높음** 수준입니다. 이 상권은 서울 전체 상권 중 해당 업종의 점포 밀도 기준 상위 33%에 해당하는 높은 점포 밀도를 보입니다.")
        elif level == "보통":
            st.info(f"**{selected_industry}** 업종의 경쟁 강도가 **보통** 수준입니다. 적절한 수준의 경쟁 환경을 유지하고 있습니다.")
        else:
            st.success(f"**{selected_industry}** 업종의 경쟁 강도가 **낮음** 수준입니다. 상대적으로 경쟁이 덜한 환경입니다.")


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