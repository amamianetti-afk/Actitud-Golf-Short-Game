import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="Actitud Golf", page_icon="⛳")

# --- CONEXIÓN DIRECTA ---
# Usamos el modo de acceso por URL que es más simple para empezar
def save_to_gsheet(nueva_fila_dict):
    try:
        # Buscamos el link del secreto
        url = st.secrets["connections"]["gsheets"]["spreadsheet"]
        
        # Intentamos conectar de forma pública/editor
        gc = gspread.public_api() 
        sh = gc.open_by_url(url)
        worksheet = sh.get_worksheet(0) # La primera hoja
        
        # Convertimos el diccionario a una lista de valores
        valores = list(nueva_fila_dict.values())
        worksheet.append_row(valores)
        return True
    except Exception as e:
        st.error(f"Error técnico: {e}")
        return False

st.title("⛳ Actitud Golf Short Game Master")

with st.sidebar:
    modo = st.radio("Entorno:", ["Práctica", "Juego en Cancha"])
    fecha = st.date_input("Fecha", datetime.now())

tab1, tab2 = st.tabs(["🎯 Putt Corto", "📏 Lag Putting"])

with tab1:
    dist = st.selectbox("Distancia:", ["35cm", "70cm", "1m", "1.5m", "2m"])
    c1, c2 = st.columns(2)
    intentos = c1.number_input("Intentos", 1, 100, 10)
    aciertos = c2.number_input("Aciertos", 0, intentos, 0)
    
    if st.button("💾 Guardar Putt"):
        datos = {
            "Fecha": str(fecha), "Entorno": modo, "Tipo": "Putt Corto",
            "Subcategoria": dist, "Intentos": intentos, "Aciertos": aciertos,
            "Cerca": 0, "Media": 0, "Lejos": 0
        }
        if save_to_gsheet(datos):
            st.success("¡Putt guardado!")
            st.balloons()

with tab2:
    rango = st.selectbox("Rango:", ["Lag A (2.5-8m)", "Lag B (8.5-15m)", "Lag C (15.5-25m)"])
    c1, c2, c3 = st.columns(3)
    cerca = c1.number_input("< 1m", 0, 10, 0)
    media = c2.number_input("1m a 1.5m", 0, 10, 0)
    lejos = c3.number_input("> 1.5m", 0, 10, 0)
    
    if (cerca + media + lejos) == 10:
        if st.button("💾 Guardar Lag"):
            datos = {
                "Fecha": str(fecha), "Entorno": modo, "Tipo": "Lag Putting",
                "Subcategoria": rango, "Intentos": 10, "Aciertos": 0,
                "Cerca": cerca, "Media": media, "Lejos": lejos
            }
            if save_to_gsheet(datos):
                st.success("¡Lag guardado!")
                st.balloons()
    else:
        st.warning("Suma 10 bolas para guardar.")
