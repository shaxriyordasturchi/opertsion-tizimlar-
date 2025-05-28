import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.header("Lab 7: Trafik yuklama balanslash")

    num_channels = st.slider("Kanal soni", 1, 10, 5)
    traffic_load = st.number_input("Umumiy trafik yuklamasi (Erlangs)", 0.0, 50.0, 20.0, 0.5)

    balanced_load = traffic_load / num_channels

    loads = np.random.normal(balanced_load, balanced_load*0.1, num_channels)
    loads = np.clip(loads, 0, None)

    fig, ax = plt.subplots()
    ax.bar(range(1, num_channels + 1), loads, color='green')
    ax.set_xlabel("Kanal raqami")
    ax.set_ylabel("Trafik yuklamasi (Erlangs)")
    ax.set_title("Trafik yuklama balanslash")

    st.pyplot(fig)

    st.write(f"Kanallarga taqsimlangan yuklama o‘rtachasi: {np.mean(loads):.2f} Erlangs")
    st.info("Yuklamalar har bir kanal uchun taxminan teng taqsimlanishi tizim samaradorligini oshiradi.")
