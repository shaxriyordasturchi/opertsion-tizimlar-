import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def run():
    st.header("Lab 10: Trafikni prognozlash mashina o‘rganishi")

    np.random.seed(1)
    periods = st.slider("Davrlar soni", 10, 100, 30)
    traffic = 2 + 0.5 * np.arange(periods) + np.random.normal(0, 2, periods)

    df = pd.DataFrame({'time': np.arange(periods), 'traffic': traffic})
    st.line_chart(df.set_index('time'))

    # Mashina o‘rganish modeli: chiziqli regressiya
    model = LinearRegression()
    X = df[['time']]
    y = df['traffic']
    model.fit(X, y)

    future_periods = st.number_input("Prognoz qilish davrlar soni", 1, 20, 5)
    X_future = np.arange(periods, periods + future_periods).reshape(-1,1)
    forecast = model.predict(X_future)

    forecast_df = pd.DataFrame({'time': np.arange(periods, periods + future_periods), 'forecast': forecast})

    st.write("Prognoz natijalari:")
    st.dataframe(forecast_df)

    plt.figure(figsize=(10,4))
    plt.plot(df['time'], df['traffic'], label='Asosiy trafik')
    plt.plot(forecast_df['time'], forecast_df['forecast'], label='Prognoz', linestyle='--')
    plt.legend()
    st.pyplot(plt)
    plt.clf()

    st.info("Chiziqli regressiya modeli vaqt ketma-ketligidagi trafikni prognozlash uchun ishlatiladi.")
