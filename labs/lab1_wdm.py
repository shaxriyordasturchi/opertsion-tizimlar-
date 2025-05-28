import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.header("Lab 1: WDM tizimida trafik modellash")

    num_channels = st.slider("Kanal soni", 1, 16, 8)
    traffic_load = st.number_input("Trafik yuklamasi (Erlangs)", min_value=0.0, max_value=20.0, value=3.0, step=0.1)

    st.write(f"Tanlangan kanal soni: {num_channels}")
    st.write(f"Trafik yuklamasi: {traffic_load} Erlangs")

    arrivals = np.random.poisson(traffic_load, num_channels)

    fig, ax = plt.subplots()
    ax.bar(range(1, num_channels + 1), arrivals, color='skyblue')
    ax.set_xlabel("Kanal raqami")
    ax.set_ylabel("Kelgan so‘rovlar soni")
    ax.set_title("WDM trafik modeli")

    st.pyplot(fig)

    avg_arrivals = np.mean(arrivals)
    var_arrivals = np.var(arrivals)

    st.write(f"O‘rtacha kelgan so‘rovlar soni: {avg_arrivals:.2f}")
    st.write(f"Dispersiya: {var_arrivals:.2f}")

    st.info("Poisson taqsimoti trafik so‘rovlarining tasodifiyligi va o‘rtacha yuklamani ifodalaydi. Kanal soni oshgani sayin tizimning qamrovi kengayadi.")
