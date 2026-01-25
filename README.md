# 🗺️ 장사잘될지도

**서울 상권 데이터 기반 입지 분석 & 창업 의사결정 플랫폼**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 목차

- [프로젝트 소개](#-프로젝트-소개)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술 스택)
- [설치 및 실행](#-설치-및-실행)
- [데이터 설명](#-데이터-설명)
- [프로젝트 구조](#-프로젝트-구조)
- [사용 방법](#-사용-방법)
- [머신러닝 모델](#-머신러닝-모델)
- [라이선스](#-라이선스)

---

## 프로젝트 소개

**장사잘될지도**는 서울시 상권분석서비스 공공데이터를 활용하여 예비 창업자들이 데이터 기반으로 합리적인 의사결정을 내릴 수 있도록 돕는 상권 분석 플랫폼입니다.

### 해결하고자 하는 문제

- **정보의 비대칭**: 창업 초보자들이 접근하기 어려운 상권 데이터
- **불확실성**: 막연한 감이 아닌 데이터 기반 의사결정 필요
- **복잡성**: 방대한 공공데이터를 직관적으로 이해하기 어려움

### 핵심 가치

**사람들이 많은지** - 유동인구, 상주인구, 직장인구 분석  
**경쟁이 심하지 않은지** - 업종별 점포 밀도 및 포화도 분석  
**앞으로도 괜찮을지** - 머신러닝 기반 매출/포화도 전망 예측

---

## 주요 기능

### 1. 홈 화면
- 플랫폼 개요 및 사용 가이드
- **AI 자영업 선배 챗봇**: OpenAI GPT-4.1-mini 기반 창업 상담 챗봇
- 빠른 질문 템플릿 (상권 분석 핵심, 초보 실수 TOP3 등)

### 2. 상권 개요
- **인터랙티브 지도**: Folium 기반 상권 경계 시각화
- **인구 구성 분석**: 
  - 상주인구 vs 직장인구 비율
  - 성별/연령대별 분포 (Plotly 차트)
- **시간대별 유동인구**: 요일/시간대별 인구 변동 히트맵
- **업종별 점포 현황**: 서비스업종별 점포 수 분포

### 3. 시장 환경
- **경쟁 강도 분석**:
  - 점포 밀도 계산 (점포수/km²)
  - 서울시 전체 대비 33/66 분위수 기반 등급 (낮음/보통/높음)
- **매출 분석**:
  - 업종별 분기별 매출 추이 (2020-2024)
  - 결제 수단별 매출 비중 (카드/현금)
  - 요일별/시간대별/성별/연령대별 매출 분포
- **집객시설**: 주변 학교, 지하철역, 관공서, 백화점 등 정보

### 4. 상권 전망
- **머신러닝 예측 모델**:
  - **매출 방향성 예측**: 증가/유지/감소
  - **시장 포화도 예측**: 포화/적정/성장
  - **상권 변화 예측**: 상승/정체/하락
- **종합 창업 적합도 점수**: 0-100점 스케일
- **분기별 예측 추이 그래프** (2025년 4분기까지)

---

## 🛠 기술 스택

### Frontend & Visualization
- **Streamlit**: 웹 애플리케이션 프레임워크
- **Plotly**: 차트 및 그래프
- **Folium**: 지도 시각화 (GeoJSON, Shapefile 지원)
- **Matplotlib**: 정적 그래프 생성

### Data Processing
- **Pandas**: 데이터 처리 및 분석
- **NumPy**: 수치 계산
- **GeoPandas**: 공간 데이터 처리

### Machine Learning
- **Scikit-learn**: 머신러닝 모델 학습 및 예측
- **Joblib**: 학습한 모델을 파일로 저장·불러오기

### AI & LLM
- **OpenAI GPT-4.1-mini**: 창업 상담 챗봇

---

## 설치 및 실행

### 1. 저장소 클론

```bash
git clone https://github.com/yourusername/trade_area_analysis.git
cd trade_area_analysis
```

### 2. 가상환경 생성 (권장)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 필요 패키지 설치

```bash
pip install streamlit pandas numpy plotly folium streamlit-folium geopandas shapely scikit-learn joblib openai
```

### 4. API 키 설정

`.streamlit/secrets.toml` 파일에 OpenAI API 키 추가:

```toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

### 5. 애플리케이션 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속

---

## 데이터 설명

### 서울시 상권분석서비스 데이터 (서울 열린데이터 광장)

| 데이터셋 | 설명 | 주요 컬럼 |
|---------|------|----------|
| **영역-상권** | 상권 경계 및 면적 정보 | 상권코드, 영역면적, 좌표(위/경도) |
| **상주인구-상권** | 성별/연령대별 거주 인구 | 총생활인구수, 남성/여성, 연령대별 |
| **직장인구-상권** | 직장인 인구 데이터 | 총직장인구수, 성별/연령대별 |
| **길단위인구-상권** | 시간대별 유동인구 | 요일별/시간대별 인구 |
| **점포-상권** | 업종별 점포 현황 | 서비스업종코드명, 점포수, 개폐업 |
| **추정매출-상권** | 업종별 매출 추정치 | 당월매출금액, 결제수단별, 요일/시간대별 |
| **집객시설-상권** | 주변 편의시설 | 학교수, 지하철역수, 관공서수 등 |
| **상권변화지표-상권** | 상권 트렌드 지표 | 매출증감률, 폐업률, 성장/쇠퇴 |

### 데이터 기간
- **2020년 1분기 ~ 2025년 2분기** (분기별 업데이트)

### Shapefile 데이터
- `서울시_상권분석서비스_영역-상권_.shp`: 상권 경계 폴리곤 (WGS84로 변환)

---

## 프로젝트 구조

```
trade_area_analysis/
│
├── app.py                      # 메인 애플리케이션 (페이지 라우팅)
├── app_home.py                 # 홈 화면 (챗봇 포함)
├── app_overview.py             # 상권 개요 페이지
├── app_environment.py          # 시장 환경 페이지
├── app_forecast.py             # 상권 전망 페이지 (ML 예측)
│
├── components/
│   └── sidebar.py              # 사이드바 필터 컴포넌트
│
├── data/
│   ├── *.csv                   # 서울시 상권 데이터셋
│   ├── *.shp                   # Shapefile (상권 경계)
│   ├── 점포-상권/              # 연도별 점포 데이터
│   ├── 추정매출 세분화/         # 연도별 매출 데이터
│   └── models/                 # 학습된 ML 모델 (pkl)
│       ├── model_sales_direction.pkl
│       ├── model_saturation.pkl
│       └── model_change_state.pkl
│
├── .streamlit/
│   └── secrets.toml            # API 키 저장
│
└── README.md                   # 프로젝트 문서
```

---

## 📖 사용 방법

### Step 1: 상권 및 업종 선택
사이드바에서:
1. **자치구** 선택 (예: 강남구)
2. **행정동** 선택 (예: 역삼동)
3. **상권** 선택 (예: 강남역 상권)
4. **서비스업종** 선택 (예: 한식음식점)

### Step 2: 순차적 분석
1. **상권 개요**: 인구 구성, 유동인구 패턴 파악
2. **시장 환경**: 경쟁 강도, 매출 현황 분석
3. **상권 전망**: 미래 예측 및 창업 적합도 확인

### Step 3: AI 챗봇 상담
- 홈 화면에서 "자영업 선배 챗봇"과 창업 관련 질문
- 빠른 질문 버튼으로 핵심 조언 즉시 확인

---

## 머신러닝 모델

### 모델 구조
- **알고리즘**: Scikit-learn Pipeline (StandardScaler + Classifier/Regressor)
- **학습 데이터**: 2020-2024년 상권별/업종별 시계열 데이터

### 예측 모델

#### 1. 매출 방향성 예측 (`model_sales_direction.pkl`)
- **목표**: 다음 분기 매출 증가/유지/감소 예측
- **입력**: 매출 추이, 점포 수 변화, YoY ( Year over Year ) 변화율
- **출력**: 3개 클래스 (증가/유지/감소)

#### 2. 시장 포화도 예측 (`model_saturation.pkl`)
- **목표**: 시장 성장 가능성 판단
- **입력**: 점포 밀도, 개폐업률, 경쟁 강도
- **출력**: 3개 클래스 (포화/적정/성장)

#### 3. 상권 변화 예측 (`model_change_state.pkl`)
- **목표**: 상권 트렌드 예측
- **입력**: 매출증감률, 폐업률, 인구 변화
- **출력**: 3개 클래스 (상승/정체/하락)

### 창업 적합도 판단 기준
창업 적합도는 머신러닝 예측 결과를 그대로 점수화하지 않고,
각 예측 결과를 창업 의사결정 관점에서 재해석한 규칙 기반 점수를 사용합니다.
**사용되는 예측 요소**

- 상권 변화 상태 (상권확장 / 정체 / 다이나믹 / 상권축소)
- 매출 방향 예측 (증가 / 유지 / 감소)
- 점포 포화 수준 (낮음 / 보통 / 높음)

---

## 개발 환경

- **Python**: 3.10
- **OS**: Windows
- **IDE**: VS Code (권장)

---

## 문의

프로젝트 관련 문의: [이메일 주소]

프로젝트 링크: [https://github.com/kmjun3203/trade_area_analysis](https://github.com/kmjun3203/trade_area_analysis)

---

- [서울 열린데이터 광장](https://data.seoul.go.kr/) - 서울시 상권분석서비스 데이터 제공
- [Streamlit](https://streamlit.io/) - 빠른 웹 앱 개발 지원
- [OpenAI](https://openai.com/) - GPT-4.1-mini API 제공

---

