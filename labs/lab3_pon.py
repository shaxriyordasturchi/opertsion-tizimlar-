import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.header("Lab 3: PON tizimi trafik tahlili")

    num_ont = st.slider("ONT qurilmalar soni", 1, 64, 32)
    traffic_per_ont = st.number_input("Har bir ONT trafik yuklamasi (Erlangs)", 0.0, 5.0, 1.0, 0.1)

    total_traffic = num_ont * traffic_per_ont
    st.write(f"Umumiy trafik yuklamasi: {total_traffic:.2f} Erlangs")

    capacity = 32.0  # Misol uchun PON kanali sig‘imi (Erlangs)
    st.write(f"Tizim sig‘imi: {capacity} Erlangs")

    overload = total_traffic / capacity
    st.write(f"Trafikning sig‘imga nisbati: {overload:.2f}")

    fig, ax = plt.subplots()
    ax.bar(['Trafik yuklamasi', 'Sig‘im'], [total_traffic, capacity], color=['green', 'blue'])
    ax.set_ylabel("Erlangs")
    ax.set_title("PON tizimi trafik tahlili")
    st.pyplot(fig)

    if overload > 1:
        st.warning("Trafik tizim sig‘imidan oshib ketgan, qo‘shimcha kanal kerak.")
    else:
        st.success("Trafik tizim sig‘imiga mos keladi.")
