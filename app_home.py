import streamlit as st
from openai import OpenAI
from pathlib import Path

# =========================
# 자영업 선배 챗봇 설정
# =========================
SYSTEM_PROMPT = """
너는 첫 창업을 준비하는 사람에게 조언해주는 현실적인 자영업 선배다.

규칙:
- 어려운 전문 용어는 쓰지 않는다.
- 숫자, 통계, 데이터는 언급하지 않는다.
- 단정적으로 말하지 않는다.
- 경험에서 나온 조언처럼 말한다.
- 한 번에 너무 많은 내용을 말하지 않는다.
- 말투는 친근한 대화체로 한다.

역할:
- 초보 창업자가 놓치기 쉬운 부분을 짚어준다.
- 겁만 주지 않고 현실적으로 말한다.
- 최종 판단은 항상 사용자에게 맡긴다.
""".strip()

QUICK_QUESTIONS = {
    "상권 볼 때 핵심": "첫 창업 기준에서 상권 볼 때 제일 중요하게 봐야 할 포인트를 알려줘.",
    "돈 관리 / 고정비": "첫 창업자가 고정비 관리할 때 제일 조심해야 할 점을 알려줘.",
    "초보 실수 TOP3": "초보 창업자가 가장 많이 하는 실수 TOP3만 현실적으로 말해줘.",
    "계약 전 체크리스트": "가게 계약하기 전에 초보 창업자가 꼭 확인해야 할 것들만 알려줘.",
    "1인 운영 가능?": "1인 창업이 가능한 경우랑 힘든 경우를 현실적으로 설명해줘.",
    "초반 마케팅 뭐부터?": "마케팅 잘 모르는 초보 창업자가 처음에 하면 좋은 것부터 알려줘.",
}

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def _ask_senior_and_append(user_text: str):
    """유저 메시지 추가 → LLM 응답 받아서 추가"""
    st.session_state.senior_messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *st.session_state.senior_messages
        ],
    )

    reply = response.choices[0].message.content
    st.session_state.senior_messages.append({"role": "assistant", "content": reply})


def run_home():
    st.title("서울 상권 분석 대시보드")

    # 메인 소개
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 30px; border-radius: 10px; margin-bottom: 30px;'>
        <h3 style='color: #1f77b4; margin-bottom: 20px;'>서울시 상권 데이터를 기반으로</h3>
        <p style='font-size: 18px; line-height: 1.8;'>
            ✔ 사람들이 많은지<br>
            ✔ 경쟁이 심하지 않은지<br>
            ✔ 앞으로도 괜찮을지<br>
            <strong>를 분석해 창업 판단을 돕는 서비스입니다</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 사용 방법
    st.markdown("### 사용 방법")
    st.info("""
    **① 사이드바에서 상권과 업종을 선택하세요**

    **② 상권 개요 → 시장 환경 → 상권 전망 순서로 확인하세요**

    **③ 최종 창업 적합도 점수를 확인하세요**
    """)

    # 추천 대상
    st.markdown("### 👤 이런 분들께 추천합니다")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style='background-color: #e8f4f8; padding: 20px; border-radius: 10px; text-align: center;'>
            <p>자영업 창업을<br>고민 중인 분</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background-color: #e8f4f8; padding: 20px; border-radius: 10px; text-align: center;'>
            <p>상권 비교를<br>데이터로 하고 싶은 분</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='background-color: #e8f4f8; padding: 20px; border-radius: 10px; text-align: center;'>
            <p>감이 아니라<br>근거로 결정하고 싶은 분</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.markdown("---")

    # =========================
    # 💬 자영업 선배 챗봇 섹션 (홈 화면)
    # =========================
    st.markdown("## 자영업 선배")
    st.markdown("""
    <div style='background-color: #f8f9fa; padding: 18px; border-radius: 10px; border-left: 4px solid #667eea;'>
        <p style='margin: 0; font-size: 15px; line-height: 1.7; color: #495057;'>
            <strong>첫 창업이 막막할 때</strong> 편하게 물어보세요.<br>
            숫자나 분석 말고, <strong>초보가 자주 놓치는 포인트</strong>를 현실적으로 정리해드립니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # 세션 초기화 (홈 화면 챗봇 전용)
    if "senior_messages" not in st.session_state:
        st.session_state.senior_messages = [
            {"role": "assistant", "content": "처음 창업이면 다들 같은 데서 막혀.\n상권, 돈, 운영… 뭐부터 궁금해?"}
        ]

    # 빠른 선택 버튼
    st.markdown("#### 🔍 빠르게 물어보기")
    cols = st.columns(3)
    for idx, (label, question) in enumerate(QUICK_QUESTIONS.items()):
        with cols[idx % 3]:
            if st.button(label, use_container_width=True, key=f"quick_{idx}"):
                _ask_senior_and_append(question)
                st.rerun()

    st.write("")
    st.divider()

    # 대화 표시
    for msg in st.session_state.senior_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # 입력
    if user_input := st.chat_input("편하게 물어봐", key="senior_chat_input"):
        _ask_senior_and_append(user_input)
        st.rerun()
