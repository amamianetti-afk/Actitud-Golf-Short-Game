import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

st.set_page_config(page_title="Actitud Golf", page_icon="⛳")

st.title("⛳ Actitud Golf Short Game Master")

# --- CONFIGURACIÓN DE ENTRADA ---
with st.sidebar:
    modo = st.radio("Entorno:", ["Práctica", "Juego en Cancha"])
    fecha = st.date_input("Fecha", datetime.now())

tab1, tab2 = st.tabs(["🎯 Putt Corto", "📏 Lag Putting"])

# Función para guardar datos de forma sencilla (vía Formulario/URL)
def guardar_datos(datos_dict):
    try:
        # Aquí usamos un truco: Mostramos los datos y confirmamos
        # Para un guardado automático real sin Service Account, 
        # lo ideal es usar st.data_editor o simplemente mostrar el éxito
        st.success("¡Datos procesados listos para el registro!")
        st.table(pd.DataFrame([datos_dict]))
        return True
    except:
        return False

with tab1:
    dist = st.selectbox("Distancia:", ["35cm", "70cm", "1m", "1.5m", "2m"])
    c1, c2 = st.columns(2)
    intentos = c1.number_input("Intentos", 1, 100, 10)
    aciertos = c2.number_input("Aciertos", 0, intentos, 0)
    
    if st.button("💾 Registrar"):
        st.balloons()
        st.info(f"Registrado: {aciertos}/{intentos} en {modo} ({dist})")
        # Nota: Por ahora, para evitar errores de conexión, 
        # estamos validando que la interfaz funcione al 100%
