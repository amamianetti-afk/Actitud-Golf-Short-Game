import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Actitud Golf", page_icon="⛳", layout="wide")

# --- CONFIG ---
URL = "https://script.google.com/macros/s/AKfycbwCue3cavrYDkwxesQrcetNM8qId7OiCh5Ez-qoJuCnSULsvWAWPlezpNao6tCsLU1k/exec"
S_ID = "1p3vWVzoHAgMk4bHY6OL3tnQLPhclGqcYspkwTw0AjFU"

# --- ALUMNOS ---
JUGADORES = ["Seleccionar...", "Agustin", "Andres", "Carlos Garcia", "Maria Lopez"]

if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    st.title("⛳ Actitud Golf")
    sel = st.selectbox("¿Quién eres?", JUGADORES)
    if st.button("Entrar"):
        if sel != "Seleccionar...":
            st.session_state['user'] = sel
            st.rerun()
    st.stop()

user = st.session_state['user']
st.sidebar.title(f"👤 {user}")
if st.sidebar.button("Salir"):
    st.session_state['user'] = None
    st.rerun()

def leer(hoja):
    try:
        u = f"https://docs.google.com/spreadsheets/d/{S_ID}/gviz/tq?tqx=out:csv&sheet={hoja}"
        df = pd.read_csv(u)
        # Limpieza crítica: quitamos espacios y tildes de los nombres de columnas
        df.columns = df.columns.str.strip().str.replace('ì', 'i').str.replace('í', 'i').str.title()
        return df[df['Nombre'] == user] if 'Nombre' in df.columns else pd.DataFrame()
    except:
        return pd.DataFrame()

# --- MENU ---
menu = st.sidebar.radio("Menú:", ["Cargar Datos", "📊 Estadísticas"])
modo = st.sidebar.radio("Entorno:", ["Práctica", "Cancha"])
fecha = str(st.sidebar.date_input("Fecha", datetime.now()))

if menu == "Cargar Datos":
    t1, t2 = st.tabs(["🎯 Corto", "📏 Lag"])
    with t1:
        if modo == "Práctica":
            d = st.selectbox("Dist:", ["35cm", "70cm", "1m", "1.5m", "2m"])
            i = st.number_input("Intentos", 1, 100, 10)
            a = st.number_input("Aciertos", 0, i, 0)
            if st.button("Guardar P. Corto"):
                js = {"nombre":user,"fecha":fecha,"entorno":modo,"tipo":"Putt Corto","subcategoria":d,"intentos":i,"aciertos":a}
                requests.post(URL, json=js)
                st.success("¡Guardado!")
        else:
            can = st.text_input("Cancha", key="c1")
            ho = st.number_input("Hoyo", 1, 18, 1)
            res = st.selectbox("Result:", ["Emboqué", "Corta", "Derecha", "Izquierda", "Larga"])
            if st.button("Guardar C. Corto"):
                js = {"nombre":user,"fecha":fecha,"entorno":modo,"tipo":"Putt Corto","cancha":can,"hoyo":ho,"resultado":res}
                requests.post(URL, json=js)
                st.success("¡Registrado!")

    with t2:
        if modo == "Práctica":
            ran = st.selectbox("Rango:", ["Lag A", "Lag B", "Lag C"])
            t_1, t_2, t_3 = "menos de 1 metro", "entre un metro y un metro y medio", "mas de un metro y medio"
            v1 = st.number_input(t_1, 0, 10, 0)
            v2 = st.number_input(t_2, 0, 10, 0)
            v3 = st.number_input(t_3, 0, 10, 0)
            if st.button("Guardar P. Lag"):
                if (v1+v2+v3==10):
                    js = {"nombre":user,"fecha":fecha,"entorno":modo,"tipo":"Lag Putting","subcategoria":ran,t_1:v1,t_2:v2,t_3:v3}
                    requests.post(URL, json=js)
                    st.success("¡Guardado!")
                else: st.error("Suma debe ser 10")
        else:
            can2 = st.text_input("Cancha", key="c2")
            res2 = st.selectbox("Result:", ["Emboqué", "Menos de 1m", "Entre 1m y 1.5m", "Mas de 1.5m"])
            if st.button("Guardar C. Lag"):
                js = {"nombre":user,"fecha":fecha,"entorno":modo,"tipo":"Lag Putting","cancha":can2,"resultado":res2}
                requests.post(URL, json=js)
                st.success("¡Registrado!")

else:
    st.header(f"📊 Reporte: {user}")
    st.subheader("🛠️ Práctica")
    c1, c2 = st.columns(2)
    
    # --- ESTADISTICAS PUTT CORTO ---
    df1 = leer("Putt_Corto")
    if not df1.empty and 'Subcategoria' in df1.columns:
        res = df1.groupby('Subcategoria').agg({'Aciertos':'sum','Intentos':'sum'}).reset_index()
        res['%'] = (res['Aciertos']/res['Intentos'])*100
        c1.plotly_chart(px.bar(res, x='Subcategoria', y='%', range_y=[0,105], text='%'))
    else:
        c1.info("No hay datos de Putt Corto")

    # --- ESTADISTICAS LAG ---
    df2 = leer("Lag_Putting")
    if not df2.empty:
        cols = ["Menos De 1 Metro", "Entre Un Metro Y Un Metro Y Medio", "Mas De Un Metro Y Medio"]
        existentes = [c for c in cols if c in df2.columns]
        if existentes:
            vals = [df2[c].sum() for c in existentes]
            c2.plotly_chart(px.pie(values=vals, names=existentes, hole=0.4))
        else:
            c2.info("No hay datos de Lag")
    
    st.divider()
    st.subheader("🏌️ Cancha")
    c3, c4 = st.columns(2)
    df3 = leer("Putt_Corto_Cancha")
    if not df3.empty and 'Resultado' in df3.columns:
        c3.plotly_chart(px.histogram(df3, x="Resultado"))
    df4 = leer("Lag_Cancha")
    if not df4.empty and 'Resultado' in df4.columns:
        c4.plotly_chart(px.pie(df4, names="Resultado"))
