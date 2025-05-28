import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

def run():
    st.header("Lab 5: Trafikning vaqt bo‘yicha prognozi")

    np.random.seed(42)
    periods = st.slider("Davrlar soni (kunlarda)", 10, 100, 50)
    traffic_level = st.number_input("Trafik asosiy darajasi", 0.0, 10.0, 3.0, 0.1)

    # Hozirgi kundan boshlab vaqt oralig'i
    start_date = pd.Timestamp.today().normalize()
    time_index = pd.date_range(start=start_date, periods=periods, freq='D')

    # Trafik ma’lumotlarini generatsiya qilish
    traffic_data = traffic_level + np.random.normal(0, 1, periods)
    df = pd.DataFrame({'Traffic': traffic_data}, index=time_index)

    # Asosiy grafik
    st.line_chart(df)

    # ARIMA modeli va prognoz
    model = ARIMA(df['Traffic'], order=(1, 0, 0))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=5)
    st.write("Keyingi 5 kun uchun trafik prognozi:")
    st.write(forecast)

    # Prognoz grafikasi
    forecast_index = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=5, freq='D')

    plt.figure(figsize=(10, 4))
    plt.plot(df.index, df['Traffic'], label='Asosiy ma\'lumot')
    plt.plot(forecast_index, forecast, label='Prognoz', linestyle='--', marker='o')
    plt.xlabel("Sana")
    plt.ylabel("Trafik")
    plt.title("Trafik prognozi (ARIMA)")
    plt.legend()
    st.pyplot(plt)
    plt.clf()

    st.info("ARIMA modeli vaqt bo‘yicha trafikni prognozlash uchun ishlatiladi.")
