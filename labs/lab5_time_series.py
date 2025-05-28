import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

def run():
    st.header("Lab 5: Trafikning vaqt bo‘yicha prognozi")

    np.random.seed(42)
    periods = st.slider("Davrlar soni", 10, 100, 50)
    traffic_level = st.number_input("Trafik asosiy darajasi", 0.0, 10.0, 3.0, 0.1)

    # Simulyatsiya qilingan vaqt seriyasi
    time_index = pd.date_range(start='2025-05-28', start='2025-06-10', periods=periods, freq='D')
    traffic_data = traffic_level + np.random.normal(0, 1, periods)

    df = pd.DataFrame({'Traffic': traffic_data}, index=time_index)

    st.line_chart(df)

    # ARIMA modeli yordamida prognoz
    model = ARIMA(df['Traffic'], order=(1,0,0))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=5)
    st.write("Keyingi 5 kun uchun trafik prognozi:")
    st.write(forecast)

    # Prognozni chizish
    plt.figure(figsize=(10,4))
    plt.plot(df.index, df['Traffic'], label='Asosiy ma\'lumot')
    plt.plot(pd.date_range(df.index[-1], periods=6, freq='D')[1:], forecast, label='Prognoz', linestyle='--')
    plt.legend()
    st.pyplot(plt)
    plt.clf()

    st.info("ARIMA modeli vaqt bo‘yicha trafikni prognozlash uchun ishlatiladi.")
