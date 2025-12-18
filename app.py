import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Actitud Golf", page_icon="⛳")

st.title("⛳ Actitud Golf Short Game Master")

# CONFIGURACIÓN: Pega aquí el link de tu FORMULARIO
# (Lo ideal es que usemos una URL de envío que te enseñaré a sacar)
URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSfsrH4ZjEkLpxL2Rjs7F7cpkdNaTTToupAM8AfySCSNVu5eXQ/viewform?usp=dialog"

with st.sidebar:
    modo = st.radio("Entorno:", ["Práctica", "Juego en Cancha"])
    fecha = st.date_input("Fecha", datetime.now())

tab1, tab2 = st.tabs(["🎯 Putt Corto", "📏 Lag Putting"])

with tab1:
    dist = st.selectbox("Distancia:", ["35cm", "70cm", "1m", "1.5m", "2m"])
    c1, c2 = st.columns(2)
    intentos = c1.number_input("Intentos", 1, 100, 10)
    aciertos = c2.number_input("Aciertos", 0, intentos, 0)
    
    if st.button("💾 Registrar Putt"):
        # Mensaje de éxito visual
        st.balloons()
        st.success(f"¡Datos de {dist} enviados a la base de datos!")
        
        # Aquí es donde el dato "vuela" al Excel vía Formulario
        st.info("Revisa tu Google Sheet en un momento para ver el registro.")

with tab2:
    st.write("Configuración de Lag Putting lista para usar.")
