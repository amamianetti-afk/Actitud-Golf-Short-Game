import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Actitud Golf Pro", page_icon="⛳", layout="wide")

# CONFIGURACIÓN DE ENLACES
URL_WEB_APP = "https://script.google.com/macros/s/AKfycbwT40gujHrmqKIgDe5ckyNLCdW8CK5Cv2BF5E0eT0Hspr-vpyMSNbxiqyFoVSFVs-Ka/exec"
SHEET_ID = "1p3vWVzoHAgMk4bHY6OL3tnQLPhclGqcYspkwTw0AjFU"

def leer_hoja(sheet_name):
    # Intentamos leer con la tilde correcta o como venga del CSV
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    return pd.read_csv(url)

st.title("⛳ Actitud Golf - Tracker Pro")

menu = st.sidebar.radio("Menú:", ["Cargar Datos", "📊 Estadísticas"])
modo = st.sidebar.radio("Entorno:", ["Práctica", "Juego en Cancha"])
fecha = st.sidebar.date_input("Fecha", datetime.now())

if menu == "Cargar Datos":
    tab1, tab2 = st.tabs(["🎯 Putt Corto", "📏 Lag Putting"])
    
    with tab1:
        if modo == "Práctica":
            dist = st.selectbox("Distancia:", ["35cm", "70cm", "1m", "1.5m", "2m"])
            c1, c2 = st.columns(2)
            intentos = c1.number_input("Intentos", 1, 100, 10)
            aciertos = c2.number_input("Aciertos", 0, intentos, 0)
            if st.button("Guardar Práctica Corto"):
                datos = {"fecha": str(fecha), "entorno": modo, "tipo": "Putt Corto", "subcategoria": dist, "intentos": intentos, "aciertos": aciertos}
                requests.post(URL_WEB_APP, json=datos)
                st.success("¡Guardado!")
                st.balloons()
        else:
            cancha = st.text_input("Cancha:")
            hoyo = st.number_input("Hoyo:", 1, 18, 1)
            dist_c = st.selectbox("Distancia aprox:", ["35cm", "70cm", "1m", "1.5m", "2m", "Más"])
            res_c = st.selectbox("Resultado:", ["Emboqué", "Falle: Corta en linea", "Falle: Corta derecha", "Falle: Corta izquierda", "Falle: Larga en linea", "Falle: Larga derecha", "Falle: Larga izquierda"])
            rut = st.radio("¿Rutina?", ["Sí", "No"])
            foc = st.radio("¿Foco?", ["Sí", "No"])
            if st.button("Guardar Putt Cancha"):
                datos = {"fecha": str(fecha), "entorno": modo, "tipo": "Putt Corto", "cancha": cancha, "hoyo": hoyo, "distancia": dist_c, "resultado": res_c, "rutina": rut, "foco": foc, "comentarios": ""}
                requests.post(URL_WEB_APP, json=datos)
                st.success("¡Registrado!")
                st.balloons()

    with tab2:
        if modo == "Práctica":
            rango = st.selectbox("Rango:", ["Lag A (2.5-8m)", "Lag B (8.5-15m)", "Lag C (15.5-25m)"])
            col1, col2, col3 = st.columns(3)
            cerca = col1.number_input("< 1m", 0, 10, 0)
            media = col2.number_input("1m a 1.5m", 0, 10, 0)
            lejos = col3.number_input("> 1.5m", 0, 10, 0)
            if st.button("Guardar Práctica Lag"):
                if (cerca+media+lejos == 10):
                    datos = {"fecha": str(fecha), "entorno": modo, "tipo": "Lag Putting", "subcategoria": rango, "cerca": cerca, "media": media, "lejos": lejos}
                    requests.post(URL_WEB_APP, json=datos)
