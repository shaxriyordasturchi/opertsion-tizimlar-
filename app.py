import streamlit as st

# Laboratoriyalarni import qilamiz
from labs import lab1_wdm, lab2_ocdma, lab3_pon, lab4_hybrid,  lab5_forecast, lab6_quality, lab7_load_balancing, lab8_visualization, lab9_real_data, lab10_ml_forecast

st.title("WDM/OCDMA PON Trafik Prognozlash Laboratoriyalari")

lab_choice = st.sidebar.selectbox("Laboratoriyani tanlang", [
    "Lab 1: WDM tizimida trafik modellash",
    "Lab 2: OCDMA asosida signal uzatish",
    "Lab 3: PON tizimi trafik tahlili",
    "Lab 4: WDM/OCDMA hibrid arxitekturasi",
    "Lab 5: Trafikning vaqt bo‘yicha prognozi",
    "Lab 6: Kanalning sifat ko‘rsatkichlari",
    "Lab 7: Trafik yuklama balanslash",
    "Lab 8: Trafik oqimini visualizatsiya",
    "Lab 9: Real trafik ma’lumotlarini analiz qilish",
    "Lab 10: Trafikni prognozlash algoritmlari",
])

if lab_choice == "Lab 1: WDM tizimida trafik modellash":
    lab1_wdm.run()
elif lab_choice == "Lab 2: OCDMA asosida signal uzatish":
    lab2_ocdma.run()
elif lab_choice == "Lab 3: PON tizimi trafik tahlili":
    lab3_pon.run()
elif lab_choice == "Lab 4: WDM/OCDMA hibrid arxitekturasi":
    lab4_hybrid.run()
elif lab_choice == "Lab 5: Trafikning vaqt bo‘yicha prognozi":
    lab5_time_series.run()
elif lab_choice == "Lab 6: Kanalning sifat ko‘rsatkichlari":
    lab6_quality.run()
elif lab_choice == "Lab 7: Trafik yuklama balanslash":
    lab7_load_balancing.run()
elif lab_choice == "Lab 8: Trafik oqimini visualizatsiya":
    lab8_visualization.run()
elif lab_choice == "Lab 9: Real trafik ma’lumotlarini analiz qilish":
    lab9_real_data.run()
elif lab_choice == "Lab 10: Trafikni prognozlash algoritmlari":
    lab10_ml_forecast.run()
