import streamlit as st
import requests
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Actitud Golf Master", page_icon="⛳")

# --- TU URL DE APPS SCRIPT ---
URL_WEB_APP = "https://script.google.com/macros/s/AKfycbz7qgMMrGkR9LQ4TqNr87OW5wm0z_JIHvEWYXueRdY7N51dEisbEReSdADc8TMT31go/exec"

st.title("⛳ Actitud Golf Short Game")
st.markdown("---")

# Menú Lateral
with st.sidebar:
    st.header("Sesión")
    modo = st.radio("Entorno:", ["Práctica", "Juego en Cancha"])
    fecha = st.date_input("Fecha", datetime.now())

# Pestañas de juego
tab1, tab2 = st.tabs(["🎯 Putt Corto", "📏 Lag Putting"])

with tab1:
    dist = st.selectbox("Distancia:", ["35cm", "70cm", "1m", "1.5m", "2m"])
    c1, c2 = st.columns(2)
    intentos = c1.number_input("Intentos", 1, 100, 10)
    aciertos = c2.number_input("Aciertos", 0, intentos, 0)
    
    if st.button("💾 Guardar Registro"):
        # Preparamos los datos EXACTAMENTE como los espera el Script
        datos = {
            "fecha": str(fecha),
            "entorno": modo,
            "tipo": "Putt Corto",
            "subcategoria": dist,
            "intentos": intentos,
            "aciertos": aciertos
        }
        
        with st.spinner('Enviando a Google Sheets...'):
            try:
                # Enviamos los datos
                response = requests.post(URL_WEB_APP, json=datos)
                if response.status_code == 200:
                    st.success("¡Logrado! Revisa tu Excel.")
                    st.balloons()
                else:
                    st.error("El servidor respondió con un error. Revisa los permisos del Script.")
            except Exception as e:
                st.error(f"Error de conexión: {e}")

with tab2:
    st.write("Configuración de Lag Putting lista para usar pronto.")
