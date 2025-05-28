import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run():
    st.header("Lab 8: Trafik oqimini visualizatsiya qilish")

    np.random.seed(0)
    hours = st.slider("Soatlar soni", 1, 24, 12)
    users = st.slider("Foydalanuvchilar soni", 1, 50, 20)

    data = np.random.poisson(3, (users, hours))
    df = pd.DataFrame(data, columns=[f"{i} soat" for i in range(1, hours+1)])

    st.write("Trafik ma’lumotlari jadvali:")
    st.dataframe(df)

    st.write("Trafik issiqlik xaritasi:")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(df, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
