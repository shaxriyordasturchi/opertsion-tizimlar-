import streamlit as st
import numpy as npimport streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.header("Lab 6: Kanalning sifat ko‘rsatkichlari (BER va SNR)")

    snr_db = st.slider("SNR (dB)", 0, 30, 15)
    traffic_load = st.number_input("Trafik yuklamasi (Erlangs)", 0.0, 10.0, 3.0, 0.1)

    # SNRni signal kuchiga aylantirish
    snr_linear = 10 ** (snr_db / 10)

    # Oddiy BER modeli (QPSK uchun)
    ber = 0.5 * np.exp(-snr_linear)

    st.write(f"Signal-to-Noise Ratio (SNR): {snr_db} dB")
    st.write(f"Bit Error Rate (BER): {ber:.6e}")

    # Grafik chizish
    fig, ax = plt.subplots()
    ax.bar(['BER'], [ber], color='red')
    ax.set_ylim(0, 1e-2)
    ax.set_title("Kanal sifat ko‘rsatkichlari")
    ax.set_ylabel("Bit Error Rate (BER)")

    st.pyplot(fig)

    st.info("SNR oshgani sayin BER kamayadi, ya’ni kanal sifati yaxshilanadi.")

import matplotlib.pyplot as plt

def run():
    st.header("Lab 6: Kanalning sifat ko‘rsatkichlari (BER va SNR)")

    snr_db = st.slider("SNR (dB)", 0, 30, 15)
    traffic_load = st.number_input("Trafik yuklamasi (Erlangs)", 0.0, 10.0, 3.0, 0.1)

    # SNRni signal kuchiga aylantirish
    snr_linear = 10 ** (snr_db / 10)

    # Oddiy BER modeli (QPSK uchun)
    ber = 0.5 * np.exp(-snr_linear)

    st.write(f"Signal-to-Noise Ratio (SNR): {snr_db} dB")
    st.write(f"Ber Error Rate (BER): {ber:.6f}")

    fig
