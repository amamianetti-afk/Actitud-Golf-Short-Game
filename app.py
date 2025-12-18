import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Actitud Golf Pro", page_icon="⛳", layout="wide")

# --- CONFIGURACIÓN ---
URL_WEB_APP = "https://script.google.com/macros/s/AKfycbwCue3cavrYDkwxesQrcetNM8qId7OiCh5Ez-qoJuCnSULsvWAWPlezpNao6tCsLU1k/exec"
SHEET_ID = "1p3vWVzoHAgMk4bHY6OL3tnQLPhclGqcYspkwTw0AjFU"

# --- LÓGICA DE IDENTIFICACIÓN ---
if 'nombre_jugador' not in st.session_state:
    st.session_state['nombre_jugador'] = None

if st.session_state['nombre_jugador'] is None:
    st.title("⛳ Bienvenido a Actitud Golf")
    st.write("Identifícate para registrar tu práctica.")
    input_nombre = st.text_input("Ingresa tu Nombre Completo:")
    if st.button("Comenzar"):
        if input_nombre:
            st.session_state['nombre_jugador'] = input_nombre.strip().title()
            st.rerun()
        else:
            st.warning("Por favor, ingresa un nombre para continuar.")
    st.stop()

usuario_actual = st.session_state['nombre_jugador']
st.sidebar.title(f"👤 {usuario_actual}")
if st.sidebar.button("Cerrar Sesión"):
    st.session_state['nombre_jugador'] = None
    st.rerun()

# --- FUNCIÓN DE LECTURA ---
def leer_hoja(sheet_name):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        if 'Nombre' in df.columns:
            df = df[df['Nombre'] == usuario_actual]
        return df
    except:
        return pd.DataFrame()

# --- INTERFAZ ---
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
                datos = {
                    "nombre": usuario_actual, "fecha": str(fecha), "entorno": modo, 
                    "tipo": "Putt Corto", "subcategoria": dist, 
                    "intentos": intentos, "aciertos": aciertos
                }
                requests.post(URL_WEB_APP, json=datos)
                st.success(f"¡Guardado para {usuario_actual}!")
                st.balloons()
        else:
            st.subheader("📝 Putt Corto en Cancha")
            cancha = st.text_input("Cancha:", key="cancha_pc")
            hoyo = st.number_input("Hoyo:", 1, 18, 1, key="hoyo_pc")
            dist_c = st.selectbox("Distancia aprox:", ["35cm", "70cm", "1m", "1.5m", "2m", "Más"])
            res_c = st.selectbox("Resultado:", ["Emboqué", "Falle: Corta", "Falle: Derecha", "Falle: Izquierda", "Falle: Larga"])
            if st.button("Guardar Putt Cancha"):
                datos = {
                    "nombre": usuario_actual, "fecha": str(fecha), "entorno": modo, 
                    "tipo": "Putt Corto", "cancha": cancha, "hoyo": hoyo, 
                    "distancia": dist_c, "resultado": res_c
                }
                requests.post(URL_WEB_APP, json=datos)
                st.success("Registrado en cancha.")

    with tab2:
        if modo == "Práctica":
            rango = st.selectbox("Rango:", ["Lag A (2.5-8m)", "Lag B (8.5-15m)", "Lag C (15.5-25m)"])
            col1, col2, col3 = st.columns(3)
            t1, t2, t3 = "menos de 1 metro", "entre un metro y un metro y medio", "mas de un metro y medio"
            v1 = col1.number_input(t1, 0, 10, 0)
            v2 = col2.number_input(t2, 0, 10, 0)
            v3 = col3.number_input(t3, 0, 10, 0)
            
            if st.button("Guardar Práctica Lag"):
                if (v1 + v2 + v3 == 10):
                    datos = {
                        "nombre": usuario_actual, "fecha": str(fecha), "entorno": modo, 
                        "tipo": "Lag Putting", "subcategoria": rango, t1: v1, t2: v2, t3: v3
                    }
                    requests.post(URL_WEB_APP, json=datos)
                    st.success("Sesión de Lag guardada.")
                    st.balloons()
                else:
                    st.error("La suma debe ser 10")
        else:
            st.subheader("📝 Lag en Cancha")
            cancha_l = st.text_input("Cancha:", key="cancha_lag")
            hoyo_l = st.number_input("Hoyo:", 1, 18, 1, key="hoyo_lag")
            dist_l = st.number_input("Metros al hoyo:", 3.0, 50.0, 10.0)
            res_l = st.selectbox("Resultado:", ["Emboqué", "Menos de 1m", "Entre 1m y 1.5m", "Más de 1.5m"])
            if st.button("Guardar Lag en Cancha"):
                datos = {
                    "nombre": usuario_actual, "fecha": str(fecha), "entorno": modo, 
                    "tipo": "Lag Putting", "cancha": cancha_l, "hoyo": hoyo_l, 
                    "distancia": dist_l, "resultado": res_l
                }
                requests.post(URL_WEB_APP, json=datos)
                st.success("Lag en cancha registrado.")

else: # --- ESTADÍSTICAS ---
    st.header(f"📊 Reporte: {usuario_actual}")
    col_a, col_b = st.columns(2)
    with col_a:
        df_pc = leer_hoja("Putt_Corto")
        if not df_pc.empty:
            st.subheader("🎯 Efectividad Putt Corto")
            df_res = df_pc.groupby('Subcategoria').agg({'Aciertos': 'sum', 'Intentos': 'sum'}).reset_index()
            df_res['%'] = (df_res['Aciertos'] / df_res['Intentos']) * 100
            fig = px.bar(df_res, x='Subcategoria', y='%', range_y=[0,105], text=df_res['%'].apply(lambda x: f'{x:.1f}%'))
            st.plotly_chart(fig)
    with col_b:
        df_lp = leer_hoja("Lag_Putting")
        if not df_lp.empty:
            st.subheader("📏 Control de Distancia (Lag)")
            t1, t2, t3 = "menos de 1 metro", "entre un metro y un metro y medio", "mas de un metro y medio"
            s1 = df_lp[t1].sum() if t1 in df_lp.columns else 0
            s2 = df_lp[t2].sum() if t2 in df_lp.columns else 0
            s3 = df_lp[t3].sum() if t3 in df_lp.columns else 0
            if (s1+s2+s3) > 0:
                fig2 = px.pie(values=[s1, s2, s3], names=[t1, t2, t3], hole=0.4)
                st.plotly_chart(fig2)
