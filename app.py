import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Actitud Golf Pro", page_icon="⛳", layout="wide")

# --- CONFIGURACIÓN ---
URL_WEB_APP = "https://script.google.com/macros/s/AKfycbwCue3cavrYDkwxesQrcetNM8qId7OiCh5Ez-qoJuCnSULsvWAWPlezpNao6tCsLU1k/exec"
SHEET_ID = "1p3vWVzoHAgMk4bHY6OL3tnQLPhclGqcYspkwTw0AjFU"

# --- LISTA DE ALUMNOS ---
LISTA_JUGADORES = ["Seleccionar...", "Agustin", "Andres", "Carlos Garcia", "Maria Lopez"]

if 'nombre_jugador' not in st.session_state:
    st.session_state['nombre_jugador'] = None

if st.session_state['nombre_jugador'] is None:
    st.title("⛳ Bienvenido a Actitud Golf")
    seleccion = st.selectbox("¿Quién eres?", LISTA_JUGADORES)
    if st.button("Entrar"):
        if seleccion != "Seleccionar...":
            st.session_state['nombre_jugador'] = seleccion
            st.rerun()
        else:
            st.error("Selecciona tu nombre.")
    st.stop()

usuario_actual = st.session_state['nombre_jugador']
st.sidebar.title(f"👤 {usuario_actual}")
if st.sidebar.button("Cerrar Sesión"):
    st.session_state['nombre_jugador'] = None
    st.rerun()

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
                datos = {"nombre": usuario_actual, "fecha": str(fecha), "entorno": modo, "tipo": "Putt Corto", "subcategoria": dist, "intentos": intentos, "aciertos": aciertos}
                requests.post(URL_WEB_APP, json=datos)
                st.success("¡Guardado!")
                st.balloons()
        else:
            cancha = st.text_input("Cancha:", key="cancha_pc")
            hoyo = st.number_input("Hoyo:", 1, 18, 1)
            dist_c = st.selectbox("Distancia aprox:", ["35cm", "70cm", "1m", "1.5m", "2m", "Más"])
            res_c = st.selectbox("Resultado:", ["Emboqué", "Falle: Corta", "Falle: Derecha", "Falle: Izquierda", "Falle: Larga"])
            if st.button("Guardar Putt Cancha"):
                datos = {"nombre": usuario_actual, "fecha": str(fecha), "entorno": modo, "tipo": "Putt Corto", "cancha": cancha, "hoyo": hoyo, "distancia": dist_c, "resultado": res_c}
                requests.post(URL_WEB_APP, json=datos)
                st.success("Registrado.")

    with tab2:
        if modo == "Práctica":
            rango = st.selectbox("Rango:", ["Lag A (2.5-8m)", "Lag B (8.5-15m)", "Lag C (15.5-25m)"])
            col1, col2, col3 = st.columns(3)
            t1, t2, t3 = "menos de 1 metro", "entre un metro y un metro y medio", "mas de un metro y medio"
            v1, v2, v3 = col1.number_input(t1, 0, 10, 0), col2.number_input(t2, 0, 10, 0), col3.number_input(t3, 0, 10, 0)
            if st.button("Guardar Práctica Lag"):
                if (v1 + v2 + v3 == 10):
                    datos = {"nombre": usuario_actual, "fecha": str(fecha), "entorno": modo, "tipo": "Lag Putting", "subcategoria": rango, t1: v1, t2: v2, t3: v3}
                    requests.post(URL_WEB_APP, json=datos)
                    st.success("¡Guardado!")
                    st.balloons()
                else:
                    st.error("La suma debe ser 10")
        else:
            cancha_l = st.text_input("Cancha:", key="cancha_lag")
            hoyo_l = st.number_input("Hoyo:", 1, 18, 1, key="h_l")
            dist_l = st.number_input("Metros al hoyo:", 3.0, 50.0, 10.0)
            res_l = st.selectbox("Resultado:", ["Emboqué", "Menos de 1m", "Entre 1m y 1.5m", "Más de 1.5m"])
            if st.button("Guardar Lag en Cancha"):
                datos = {"nombre": usuario_actual, "fecha": str(fecha), "entorno": modo, "tipo": "Lag Putting", "cancha": cancha_l, "hoyo": hoyo_l, "distancia": dist_l, "resultado": res_l}
                requests.post(URL_WEB_APP, json=datos)
                st.success("Registrado.")

else: # --- ESTADÍSTICAS PROTEGIDAS ---
    st.header(f"📊 Reporte: {usuario_actual}")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("🎯 Efectividad Putt Corto")
        df_pc = leer_hoja("Putt_Corto")
        if not df_pc.empty and 'Subcategoria' in df_pc.columns:
            df_res = df_pc.groupby('Subcategoria').agg({'Aciertos': 'sum', 'Intentos': 'sum'}).reset_index()
            df_res['%'] = (df_res['Aciertos'] / df_res['Intentos']) * 100
            fig = px.bar(df_res, x='Subcategoria', y='%', range_y=[0,105], text=df_res['%'].apply(lambda x: f'{x:.1f}%'))
            st.plotly_chart(fig)
        else:
            st.info("Aún no tienes datos de Putt Corto.")

    with col_b:
        st.subheader("📏 Control de Distancia (Lag)")
        df_lp = leer_hoja("Lag_Putting")
        t1, t2, t3 = "menos de 1 metro", "entre un metro y un metro y medio", "mas de un metro y medio"
        if not df_lp.empty and t1 in df_lp.columns:
            s1, s2, s3 = df_lp[t1].sum(), df_lp[t2].sum(), df_lp[t3].sum()
            if (s1+s2+s3) > 0:
                fig2 = px.pie(values=[s1, s2, s3], names=[t1, t2, t3], hole=0.4)
                st.plotly_chart(fig2)
            else:
                st.info("Registra una sesión de Lag para ver el gráfico.")
        else:
            st.info("Aún no tienes datos de Lag Putting.")
