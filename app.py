import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Actitud Golf", page_icon="⛳")

# Conexión a Google Sheets
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
    
    eficiencia = (aciertos / intentos) * 100
    st.metric("Eficacia", f"{eficiencia}%")

    if st.button("💾 Guardar Putt"):
        # Leer datos actuales
        df_existente = conn.read(ttl=0)
        
        # Crear nueva fila
        nueva_fila = pd.DataFrame([{
            "Fecha": str(fecha), "Entorno": modo, "Tipo": "Putt Corto",
            "Subcategoria": dist, "Intentos": intentos, "Aciertos": aciertos,
            "Cerca": 0, "Media": 0, "Lejos": 0
        }])
        
        # Unir y guardar
        df_final = pd.concat([df_existente, nueva_fila], ignore_index=True)
        conn.update(data=df_final)
        st.success("¡Datos guardados en Google Sheets!")
        st.balloons()

with tab2:
    rango = st.selectbox("Rango:", ["Lag A (2.5-8m)", "Lag B (8.5-15m)", "Lag C (15.5-25m)"])
    st.write("De 10 bolas, ¿dónde quedaron?")
    c1, c2, c3 = st.columns(3)
    cerca = c1.number_input("< 1m", 0, 10, 0)
    media = c2.number_input("1m a 1.5m", 0, 10, 0)
    lejos = c3.number_input("> 1.5m", 0, 10, 0)
    
    if (cerca + media + lejos) == 10:
        if st.button("💾 Guardar Lag"):
            df_existente = conn.read(ttl=0)
            nueva_fila = pd.DataFrame([{
                "Fecha": str(fecha), "Entorno": modo, "Tipo": "Lag Putting",
                "Subcategoria": rango, "Intentos": 10, "Aciertos": 0,
                "Cerca": cerca, "Media": media, "Lejos": lejos
            }])
            df_final = pd.concat([df_existente, nueva_fila], ignore_index=True)
            conn.update(data=df_final)
            st.success("¡Distribución guardada!")
    else:
        st.warning("La suma debe ser exactamente 10 bolas.")
