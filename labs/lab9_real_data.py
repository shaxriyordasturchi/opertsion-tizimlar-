import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def run():
    st.header("Lab 9: Real trafik ma’lumotlarini analiz qilish")

    uploaded_file = st.file_uploader("CSV formatida trafik ma’lumotlarini yuklang", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Ma’lumotlar jadvali:")
        st.dataframe(df.head())

        st.write("Trafik ustunlari:")
        columns = df.columns.tolist()
        x_col = st.selectbox("Vaqt ustuni", columns)
        y_col = st.selectbox("Trafik ustuni", columns)

        if st.button("Grafik chizish"):
            plt.figure(figsize=(10,4))
            plt.plot(df[x_col], df[y_col], marker='o')
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.title("Real trafik ma’lumotlari grafikasi")
            st.pyplot(plt)
            plt.clf()
