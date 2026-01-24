import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
from pathlib import Path


# -----------------------------
# 캐시: 모델 로드
# -----------------------------
@st.cache_resource
def load_models():
    models_dir = Path("../data/models")  # ✅ 여기로 변경
    pipe_sales = joblib.load(models_dir / "model_sales_direction.pkl")
    pipe_satu  = joblib.load(models_dir / "model_saturation.pkl")
    pipe_change = joblib.load(models_dir / "model_change_state.pkl")
    return pipe_sales, pipe_satu, pipe_change



# -----------------------------
# 캐시: 데이터 로드
# -----------------------------
@st.cache_data
def load_data():
    df_sales = pd.read_csv("../data/서울시 상권분석서비스(추정매출-상권)_filtered.csv", encoding="cp949")
    df_store = pd.read_csv("../data/서울시 상권분석서비스(점포-상권)_filtered.csv", encoding="cp949")
    return df_sales, df_store


def _year_from_quarter(q):
    return int(q) // 10


def build_year_features(df_sales, df_store, market_name, industry_name, target_year: int):
    """
    학습에서 썼던 입력(X)을 '연 단위'로 맞춰서 1행 만들기.
    - sales_month_avg: 해당 연도 분기별 '당월_매출_금액 합'의 평균
    - store_avg: 해당 연도 분기별 '점포_수 합'의 평균
    - sales_yoy / store_yoy: 전년 대비 변화율
    """
    # ---- sales (해당 연도)
    s = df_sales[
        (df_sales["상권_코드_명"] == market_name) &
        (df_sales["서비스_업종_코드_명"] == industry_name)
    ].copy()

    if s.empty:
        return None  # 매출 데이터 자체가 없음

    s["year"] = s["기준_년분기_코드"].apply(_year_from_quarter)
    s_y = s[s["year"] == target_year]
    s_py = s[s["year"] == (target_year - 1)]

    # 분기별 합 → 평균(연 단위 대표값)
    sales_month_avg = (
        s_y.groupby("기준_년분기_코드")["당월_매출_금액"].sum().mean()
        if not s_y.empty else None
    )
    prev_sales_month_avg = (
        s_py.groupby("기준_년분기_코드")["당월_매출_금액"].sum().mean()
        if not s_py.empty else None
    )

    # ---- store (해당 연도)
    t = df_store[
        (df_store["상권_코드_명"] == market_name) &
        (df_store["서비스_업종_코드_명"] == industry_name)
    ].copy()

    t["year"] = t["기준_년분기_코드"].apply(_year_from_quarter)
    t_y = t[t["year"] == target_year]
    t_py = t[t["year"] == (target_year - 1)]

    store_avg = (
        t_y.groupby("기준_년분기_코드")["점포_수"].sum().mean()
        if not t_y.empty else None
    )
    prev_store_avg = (
        t_py.groupby("기준_년분기_코드")["점포_수"].sum().mean()
        if not t_py.empty else None
    )

    # ---- YoY
    sales_yoy = None
    if (sales_month_avg is not None) and (prev_sales_month_avg not in (None, 0)):
        sales_yoy = (sales_month_avg - prev_sales_month_avg) / prev_sales_month_avg

    store_yoy = None
    if (store_avg is not None) and (prev_store_avg not in (None, 0)):
        store_yoy = (store_avg - prev_store_avg) / prev_store_avg

    row = pd.DataFrame([{
        "sales_month_avg": sales_month_avg,
        "sales_yoy": sales_yoy,
        "store_avg": store_avg,
        "store_yoy": store_yoy,
    }])
    return row


def make_trend_chart(df, x_col, y_col, title, y_label):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode="lines+markers"
    ))
    fig.update_layout(
        title={"text": title, "x": 0.5, "xanchor": "center"},
        xaxis_title="기준_년분기_코드",
        yaxis_title=y_label,
        height=360,
        margin=dict(l=40, r=40, t=60, b=40),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    return fig


def score_risk(change_pred, sales_pred, satu_pred):
    # 상권 변화 점수 (가중치 2배)
    change_score_map = {"상권확장": 2, "정체": 0, "다이나믹": -1, "상권축소": -2}
    sales_score_map = {"INC": 1, "FLAT": 0, "DEC": -1}
    satu_score_map = {"LOW": 1, "MID": 0, "HIGH": -1}

    total = (change_score_map.get(change_pred, 0) * 2
             + sales_score_map.get(sales_pred, 0)
             + satu_score_map.get(satu_pred, 0))

    if total >= 3:
        label = "추천"
    elif total >= 1:
        label = "보통"
    else:
        label = "주의"

    return total, label


def run_forecast():
    st.write(""); st.write(""); st.write(""); st.write("")
    st.title("상권 전망")
    st.markdown("<hr style='border:none;border-top:2px dashed #ccc;margin:20px 0;'>", unsafe_allow_html=True)
    st.subheader("선택한 상권의 미래 예측 분석")

    # ✅ Session state에서 필터 정보 가져오기
    filters = st.session_state.get("filters", {})
    selected_gu = filters.get("gu")
    selected_dong = filters.get("dong")
    selected_market = filters.get("market")
    selected_industry = filters.get("industry")

    if not selected_market or not selected_industry:
        st.warning("사이드바에서 상권과 업종을 먼저 선택해줘.")
        return

    # 헤더(기존 스타일 유지)
    st.markdown(f"""
        <div style="
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin-bottom: 30px;
        ">
            <p style="color: #495057; font-size: 15px; line-height: 1.7; margin: 0;">
                📊 <strong>상권 전망 분석</strong><br>
                • 선택한 상권: <span style="color: #667eea; font-weight: 600;">{selected_market}</span><br>
                • 위치: <span style="color: #764ba2; font-weight: 600;">{selected_gu} {selected_dong}</span><br>
                • 분석 업종: <span style="color: #667eea; font-weight: 600;">{selected_industry}</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 데이터/모델 로드
    df_sales, df_store = load_data()
    pipe_sales, pipe_satu, pipe_change = load_models()

    # 최신 연도(데이터 기반)
    latest_q = int(max(df_sales["기준_년분기_코드"].max(), df_store["기준_년분기_코드"].max()))
    latest_year = latest_q // 10

    # -----------------------------
    # (공통) 시계열 데이터 준비
    # -----------------------------
    sales_ts = df_sales[
        (df_sales["상권_코드_명"] == selected_market) &
        (df_sales["서비스_업종_코드_명"] == selected_industry)
    ].groupby("기준_년분기_코드", as_index=False)["당월_매출_금액"].sum().sort_values("기준_년분기_코드")

    store_ts = df_store[
        (df_store["상권_코드_명"] == selected_market) &
        (df_store["서비스_업종_코드_명"] == selected_industry)
    ].groupby("기준_년분기_코드", as_index=False)["점포_수"].sum().sort_values("기준_년분기_코드")

    # -----------------------------
    # 2025(또는 최신연도) 입력 1행 만들기
    # -----------------------------
    X_row = build_year_features(df_sales, df_store, selected_market, selected_industry, latest_year)
    if X_row is None:
        st.error("선택한 상권/업종에 대해 예측에 필요한 데이터(매출)가 부족해.")
        return

    # 각 모델용 X (학습 때 컬럼에 맞춰서!)
    X_sales = X_row[["sales_month_avg", "sales_yoy"]]
    X_satu   = X_row[["sales_month_avg", "sales_yoy", "store_avg", "store_yoy"]]
    X_change = X_row[["sales_month_avg", "sales_yoy", "store_avg", "store_yoy"]]

    # 예측
    pred_change = pipe_change.predict(X_change)[0]
    proba_change = pipe_change.predict_proba(X_change)[0]
    change_classes = list(pipe_change.classes_)
    change_top_idx = int(pd.Series(proba_change).idxmax())
    change_conf = float(proba_change[change_top_idx])

    pred_sales = pipe_sales.predict(X_sales)[0]
    proba_sales = pipe_sales.predict_proba(X_sales)[0]
    sales_classes = list(pipe_sales.classes_)
    sales_conf = float(proba_sales[list(sales_classes).index(pred_sales)])

    pred_satu = pipe_satu.predict(X_satu)[0]
    proba_satu = pipe_satu.predict_proba(X_satu)[0]
    classes = list(pipe_satu.classes_)

    p_low = float(proba_satu[classes.index("LOW")]) if "LOW" in classes else 0.0

    # LOW 확률이 낮으면 "MID"로 보정 (MVP용)
    if pred_satu == "LOW" and p_low < 0.70:
        pred_satu = "MID"
    satu_classes = list(pipe_satu.classes_)
    satu_conf = float(proba_satu[list(satu_classes).index(pred_satu)])

    # 보기 좋은 라벨(화면용)
    sales_label_map = {"INC": "증가", "FLAT": "보합", "DEC": "감소"}
    satu_label_map = {"LOW": "여유", "MID": "보통", "HIGH": "포화"}

    st.write("")
    st.write("")
    st.write("")
    st.markdown("---")
    st.write("")
    st.write("")
    st.write("")

    # ===========================
    # 📈 1. 상권 변화 예측
    # ===========================
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <h2 style="color: white; margin: 0; text-align: center;">
                상권 변화 예측
            </h2>
            <p style="color: rgba(255,255,255,0.9); text-align: center; margin-top: 10px; font-size: 16px;">
                매출·점포 흐름 기반 상권 상태 전망
            </p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.metric("예측 결과", pred_change)
    with c2:
        st.metric("신뢰도(확률)", f"{change_conf*100:.1f}%")

    # (참고용) 점포 추이 차트 하나
    if not store_ts.empty:
        fig_store = make_trend_chart(store_ts, "기준_년분기_코드", "점포_수", "업종 점포 수 추이", "점포 수(개)")
        st.plotly_chart(fig_store, use_container_width=True)

    st.markdown("""
        <div style="background-color:#f8f9fa;padding:20px;border-radius:10px;border-left:4px solid #667eea;margin-bottom:20px;">
            <p style="margin:0;color:#495057;line-height:1.7;">
                이 예측은 “최근 흐름이 이어진다면 어떤 상태로 갈 가능성이 큰지”를 보는 용도입니다. 
                결과가 <b>다이나믹/정체</b>로 나오면 진입 시점과 운영 전략을 더 꼼꼼히 잡는 게 좋습니다.
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

    # ===========================
    # 💰 2. 매출 방향 예측
    # ===========================
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <h2 style="color: white; margin: 0; text-align: center;">
                매출 방향 예측
            </h2>
            <p style="color: rgba(255,255,255,0.9); text-align: center; margin-top: 10px; font-size: 16px;">
                선택 업종의 매출 흐름이 다음에도 이어질지 확인
            </p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.metric("예측 결과", sales_label_map.get(pred_sales, pred_sales))
    with c2:
        st.metric("신뢰도(확률)", f"{sales_conf*100:.1f}%")

    if not sales_ts.empty:
        fig_sales = make_trend_chart(sales_ts, "기준_년분기_코드", "당월_매출_금액", "업종 매출 추이", "당월 매출(원)")
        st.plotly_chart(fig_sales, use_container_width=True)


    st.write("")
    st.write("")
    st.write("")
    st.markdown("---")
    st.write("")
    st.write("")
    st.write("")

    # ===========================
    # 🏪 3. 점포 포화 예측
    # ===========================
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <h2 style="color: white; margin: 0; text-align: center;">
                점포 포화 예측
            </h2>
            <p style="color: rgba(255,255,255,0.9); text-align: center; margin-top: 10px; font-size: 16px;">
                경쟁이 더 치열해질 가능성이 있는지 체크
            </p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.metric("예측 결과", satu_label_map.get(pred_satu, pred_satu))
    with c2:
        st.metric("신뢰도(확률)", f"{satu_conf*100:.1f}%")


    st.write("")
    st.write("")
    st.write("")
    st.markdown("---")
    st.write("")
    st.write("")
    st.write("")

    # ===========================
    # ⚠️ 종합 리스크 평가 (룰 기반)
    # ===========================
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <h2 style="color: white; margin: 0; text-align: center;">
                종합 창업 리스크 평가
            </h2>
            <p style="color: rgba(255,255,255,0.9); text-align: center; margin-top: 10px; font-size: 16px;">
                3가지 예측을 합쳐서 지금 들어가도 괜찮은지 한 번 더 점검
            </p>
        </div>
    """, unsafe_allow_html=True)

    total_score, risk_label = score_risk(pred_change, pred_sales, pred_satu)

    colA, colB, colC = st.columns(3)
    with colA:
        st.metric("상권 변화", pred_change)
    with colB:
        st.metric("매출 방향", sales_label_map.get(pred_sales, pred_sales))
    with colC:
        st.metric("점포 포화", satu_label_map.get(pred_satu, pred_satu))

    st.markdown(f"""
        <div style="background-color:#ffffff;padding:20px;border-radius:12px;border:1px solid #e0e0e0;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
            <h3 style="margin:0 0 10px 0;">최종 판단: <span style="color:#667eea;">{risk_label}</span></h3>
            <p style="margin:0;color:#495057;line-height:1.7;">
                내부 점수 기준으로 <b>{total_score}</b>점이 나왔습니다. <br>
                점수는 결정이라기보다, 서로 다른 예측을 한 번에 정리해주는 <b>체크리스트</b>라고 보면 됩니다.
            </p>
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
