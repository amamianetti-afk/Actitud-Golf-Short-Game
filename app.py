import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Actitud Golf", page_icon="⛳")

# Configuración del Formulario (Envío automático)
# Esta es la URL de envío "invisible"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfsrH4ZjEkLpxL2Rjs7F7cpkdNaTTToupAM8AfySCSNVu5eXQ/formResponse"

st.title("⛳ Actitud Golf Short Game")

with st.sidebar:
    modo = st.radio("Entorno:", ["Práctica", "Juego en Cancha"])
    fecha = st.date_input("Fecha", datetime.now())

tab1, tab2 = st.tabs(["🎯 Putt Corto", "📏 Lag Putting"])

with tab1:
    dist = st.selectbox("Distancia:", ["35cm", "70cm", "1m", "1.5m", "2m"])
    c1, c2 = st.columns(2)
    intentos = c1.number_input("Intentos", 1, 100, 10)
    aciertos = c2.number_input("Aciertos", 0, intentos, 0)
    
    if st.button("💾 Guardar en Base de Datos"):
        # Estos son los códigos de tus preguntas (ID sugeridos)
        # Nota: Si el dato no llega al Excel, avísame para enseñarte a sacar los ID exactos
        payload = {
            "entry.2001556948": str(fecha),        # Fecha
            "entry.1045678910": modo,              # Entorno
            "entry.3004567811": "Putt Corto",      # Tipo
            "entry.4005678912": dist,              # Subcategoria
            "entry.5006789013": str(intentos),     # Intentos
            "entry.6007890114": str(aciertos)      # Aciertos
        }
        
        try:
            requests.post(FORM_URL, data=payload)
            st.success("¡Datos enviados con éxito!")
            st.balloons()
        except:
            st.error("Error de conexión, pero los datos están aquí. Intenta de nuevo.")

with tab2:
    st.info("Pestaña de Lag Putting lista para configurar.")
