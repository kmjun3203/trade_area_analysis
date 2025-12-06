import streamlit as st
import pandas as pd

def main():
    st.title("서울 상권 분석 대시보드")
    st.sidebar.title("기능")
    menu = ['상권 분석', 'AI예측']

    choice = st.sidebar.selectbox('메뉴', menu)

    df_area = pd.read_csv("./data/서울시_상권분석서비스_좌표변환.csv")
    

    if choice == menu[0]:
        pass
    elif choice == menu[1]:
        pass


if __name__ == '__main__':
    main()