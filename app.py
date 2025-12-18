import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Actitud Golf Master", page_icon="⛳")

# --- USA TU URL DE APPS SCRIPT ---
URL_WEB_APP = "https://script.google.com/macros/s/AKfycbykDddnOEC1Wl4ouXcRlKpcSxrscn7p4xFyxG4nVfiPHmm7ETbfLk2l0bOpk1qBeS_o/exec"

st.title("⛳ Actitud Golf Short Game")

with st.sidebar:
    st.header("Sesión")
    modo = st.radio("Entorno:", ["Práctica", "Juego en Cancha"])
    fecha = st.date_input("Fecha", datetime.now())

tab1, tab2 = st.tabs(["🎯 Putt Corto", "📏 Lag Putting"])

with tab1:
    st.subheader("Control de Distancia Corta")
    dist = st.selectbox("Distancia:", ["35cm", "70cm", "1m", "1.5m", "2m"])
    c1, c2 = st.columns(2)
    intentos = c1.number_input("Intentos", 1, 100, 10, key="p_int")
    aciertos = c2.number_input("Aciertos", 0, intentos, 0, key="p_aci")
    
    if st.button("💾 Guardar Putt"):
        datos = {
            "fecha": str(fecha), "entorno": modo, "tipo": "Putt Corto", 
            "subcategoria": dist, "intentos": intentos, "aciertos": aciertos
        }
        with st.spinner('Enviando...'):
            res = requests.post(URL_WEB_APP, json=datos)
            if res.status_code == 200:
                st.success("¡Putt Guardado!")
                st.balloons()

with tab2:
    st.subheader("Control de Lag Putting")
    rango = st.selectbox("Rango:", ["Lag A (2.5-8m)", "Lag B (8.5-15m)", "Lag C (15.5-25m)"])
    st.write("De 10 bolas, ¿dónde quedaron?")
    
    col1, col2, col3 = st.columns(3)
    cerca = col1.number_input("< 1m", 0, 10, 0, key="l_cerca")
    media = col2.number_input("1m a 1.5m", 0, 10, 0, key="l_media")
    lejos = col3.number_input("> 1.5m", 0, 10, 0, key="l_lejos")
    
    suma = cerca + media + lejos
    st.info(f"Total de bolas: {suma} / 10")
    
    if suma == 10:
        if st.button("💾 Guardar Lag"):
            datos = {
                "fecha": str(fecha), "entorno": modo, "tipo": "Lag Putting",
                "subcategoria": rango, "cerca": cerca, "media": media, "lejos": lejos
            }
            with st.spinner('Enviando...'):
                res = requests.post(URL_WEB_APP, json=datos)
                if res.status_code == 200:
                    st.success("¡Lag Putting Guardado!")
                    st.balloons()
    else:
        st.warning("⚠️ La suma de las bolas debe ser exactamente 10 para poder guardar.")
