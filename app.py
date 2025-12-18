import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Actitud Golf", page_icon="⛳")

# Conexión profesional usando los Secrets que pegaste
conn = st.connection("gsheets", type=GSheetsConnection)

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
        # Leemos los datos actuales
        df_existente = conn.read()
        
        nueva_fila = pd.DataFrame([{
            "Fecha": str(fecha), "Entorno": modo, "Tipo": "Putt Corto",
            "Subcategoria": dist, "Intentos": intentos, "Aciertos": aciertos,
            "Cerca": 0, "Media": 0, "Lejos": 0
        }])
        
        df_final = pd.concat([df_existente, nueva_fila], ignore_index=True)
        conn.update(data=df_final)
        st.success("¡Guardado con éxito!")
        st.balloons()

# (Repite la misma lógica para Lag Putting si deseas)
