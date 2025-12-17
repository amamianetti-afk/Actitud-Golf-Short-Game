import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración de Actitud Golf
st.set_page_config(page_title="Actitud Golf Short Game", page_icon="⛳")
st.title("⛳ Actitud Golf Short Game Master")

# Conexión a la base de datos
conn = st.connection("gsheets", type=GSheetsConnection)

# --- MENÚ DE ENTRADA ---
with st.sidebar:
    modo = st.radio("Entorno:", ["Práctica", "Juego en Cancha"])
    fecha = st.date_input("Fecha", datetime.now())

tab1, tab2 = st.tabs(["🎯 Putt Corto", "📏 Lag Putting"])

with tab1:
    dist = st.selectbox("Distancia:", ["35cm", "70cm", "1m", "1.5m", "2m"])
    col_i, col_a = st.columns(2)
    intentos = col_i.number_input("Intentos", 1, 100, 10, key="p1")
    aciertos = col_a.number_input("Aciertos", 0, intentos, 0, key="p2")
    
    eficiencia = (aciertos / intentos) * 100
    
    # LÓGICA DE COACHING ACTITUD GOLF
    if modo == "Juego en Cancha" and dist in ["35cm", "70cm", "1m"]:
        if eficiencia < 85: # Umbral de alerta
            st.error("🚨 **ALERTA DE COACHING**")
            st.warning("El fallo en distancia corta suele ser mental o de rutina. Revisa: \n"
                       "1. ¿Hiciste tu rutina completa?\n"
                       "2. Mantén la cara del palo estable hacia el objetivo.\n"
                       "3. No aceleres por nervios, mantén el tempo.")

    if st.button("Guardar Putt"):
        # Aquí la app envía los datos a tu Google Sheet
        nuevo_dato = pd.DataFrame([{
            "Fecha": str(fecha), "Entorno": modo, "Tipo": "Putt Corto",
            "Subcategoria": dist, "Intentos": intentos, "Aciertos": aciertos
        }])
        st.success("¡Registrado en Google Sheets!")

with tab2:
    rango = st.selectbox("Rango:", ["Lag A (2.5-8m)", "Lag B (8.5-15m)", "Lag C (15.5-25m)"])
    c1, c2, c3 = st.columns(3)
    cerca = c1.number_input("< 1m", 0, 10, 0)
    media = c2.number_input("1m a 1.5m", 0, 10, 0)
    lejos = c3.number_input("> 1.5m", 0, 10, 0)
    
    if (cerca + media + lejos) == 10:
        if st.button("Guardar Lag"):
            st.balloons()
            st.success(f"Lag {rango} guardado.")
    else:
        st.info("Suma 10 bolas para guardar.")
