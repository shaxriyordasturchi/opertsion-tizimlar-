import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.header("Lab 2: OCDMA asosida signal uzatish")

    code_length = st.slider("Kod uzunligi", 5, 50, 16)
    num_users = st.slider("Foydalanuvchilar soni", 1, 20, 8)
    traffic_per_user = st.number_input("Foydalanuvchi trafik yuklamasi (Erlangs)", 0.0, 5.0, 1.0, 0.1)

    total_traffic = num_users * traffic_per_user
    st.write(f"Umumiy trafik yuklamasi: {total_traffic:.2f} Erlangs")

    interference = total_traffic / code_length

    st.write(f"OCDMA tizimida aralashish darajasi: {interference:.3f}")

    # Grafik: interference va trafik
    plt.figure(figsize=(8,4))
    plt.bar(['Interference'], [interference], color='orange')
    st.pyplot(plt)
    plt.clf()

    st.info("OCDMA kod uzunligi oshgani sayin aralashish kamayadi, bu esa trafik sifatini yaxshilaydi.")
