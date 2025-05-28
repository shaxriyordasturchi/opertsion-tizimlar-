import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.header("Lab 4: WDM/OCDMA hibrid arxitekturasi")

    num_wdm_channels = st.slider("WDM kanallar soni", 1, 16, 8)
    num_ocdma_users = st.slider("OCDMA foydalanuvchilari soni", 1, 20, 10)
    traffic_per_user = st.number_input("Foydalanuvchi trafik yuklamasi (Erlangs)", 0.0, 5.0, 1.0, 0.1)

    total_traffic = num_ocdma_users * traffic_per_user
    st.write(f"Umumiy OCDMA trafik: {total_traffic:.2f} Erlangs")

    interference = total_traffic / num_wdm_channels

    fig, ax = plt.subplots()
    ax.bar(range(1, num_wdm_channels + 1), [interference] * num_wdm_channels, color='purple')
    ax.set_xlabel("WDM kanal raqami")
    ax.set_ylabel("Aralashish darajasi")
    ax.set_title("Hibrid WDM/OCDMA trafik aralashishi")
    st.pyplot(fig)

    st.info("Hibrid tizimda WDM kanallari trafikni bo‘lishadi, OCDMA esa aralashishni kamaytiradi.")
