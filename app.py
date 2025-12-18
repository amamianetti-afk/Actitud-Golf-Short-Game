import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuramos para que se vea bien en pantallas pequeñas
st.set_page_config(page_title="Actitud Golf", page_icon="⛳", layout="centered")

URL = "https://script.google.com/macros/s/AKfycbwCue3cavrYDkwxesQrcetNM8qId7OiCh5Ez-qoJuCnSULsvWAWPlezpNao6tCsLU1k/exec"
S_ID = "1p3vWVzoHAgMk4bHY6OL3tnQLPhclGqcYspkwTw0AjFU"

JUGADORES = ["Seleccionar...", "Agustin", "Andres", "Carlos Garcia", "Maria Lopez"]

if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    st.title("⛳ Actitud Golf")
    st.write("Selecciona tu nombre:")
    sel = st.selectbox("", JUGADORES) # Quitamos la etiqueta para ganar espacio
    if st.button("ENTRAR", use_container_width=True): # Botón ancho para dedo
        if sel != "Seleccionar...":
            st.session_state['user'] = sel
            st.rerun()
    st.stop()

user = st.session_state['user']
# En móvil la sidebar se esconde, ponemos el saludo arriba
st.write(f"Hola, **{user}** 👋")

# --- MENU MOVIL ---
menu = st.sidebar.radio("Menú:", ["Cargar Datos", "📊 Estadísticas"])
modo = st.sidebar.radio("Entorno:", ["Práctica", "Cancha"])
fecha = str(st.sidebar.date_input("Fecha", datetime.now()))

if st.sidebar.button("Cerrar Sesión"):
    st.session_state['user'] = None
    st.rerun()

def leer(hoja):
    try:
        u = f"https://docs.google.com/spreadsheets/d/{S_ID}/gviz/tq?tqx=out:csv&sheet={hoja}"
        df = pd.read_csv(u)
        df.columns = df.columns.str.strip().str.title()
        return df[df['Nombre'] == user] if 'Nombre' in df.columns else pd.DataFrame()
    except:
        return pd.DataFrame()

if menu == "Cargar Datos":
    t1, t2 = st.tabs(["🎯 CORTO", "📏 LAG"])
    
    with t1:
        if modo == "Práctica":
            d = st.selectbox("Distancia:", ["35cm", "70cm", "1m", "1.5m", "2m"])
            i = st.number_input("Intentos", 1, 100, 10)
            a = st.number_input("Aciertos", 0, i, 0)
            if st.button("GUARDAR PRÁCTICA", use_container_width=True):
                js = {"nombre":user,"fecha":fecha,"entorno":modo,"tipo":"Putt Corto","subcategoria":d,"intentos":i,"aciertos":a}
                requests.post(URL, json=js)
                st.success("¡Guardado!")
                st.balloons()
        else:
            can = st.text_input("Cancha", placeholder="Nombre del club")
            ho = st.number_input("Hoyo", 1, 18, 1)
            res = st.selectbox("Resultado:", ["Emboqué", "Corta", "Derecha", "Izquierda", "Larga"])
            if st.button("GUARDAR EN CANCHA", use_container_width=True):
                js = {"nombre":user,"fecha":fecha,"entorno":modo,"tipo":"Putt Corto","cancha":can,"hoyo":ho,"resultado":res}
                requests.post(URL, json=js)
                st.success("¡Registrado!")

    with t2:
        if modo == "Práctica":
            ran = st.selectbox("Rango:", ["Lag A", "Lag B", "Lag C"])
            v1 = st.number_input("A menos de 1m", 0, 10, 0)
            v2 = st.number_input("Entre 1m y 1.5m", 0, 10, 0)
            v3 = st.number_input("A más de 1.5m", 0, 10, 0)
            if st.button("GUARDAR LAG", use_container_width=True):
                if (v1+v2+v3==10):
                    js = {"nombre":user,"fecha":fecha,"entorno":modo,"tipo":"Lag Putting","subcategoria":ran,"menos de 1 metro":v1,"entre un metro y un metro y medio":v2,"mas de un metro y medio":v3}
                    requests.post(URL, json=js)
                    st.success("¡Guardado!")
                else: st.error("La suma debe ser 10")
        else:
            can2 = st.text_input("Cancha", key="c2")
            res2 = st.selectbox("Resultado:", ["Emboqué", "Menos de 1m", "Entre 1m y 1.5m", "Mas de 1.5m"])
            if st.button("GUARDAR LAG CANCHA", use_container_width=True):
                js = {"nombre":user,"fecha":fecha,"entorno":modo,"tipo":"Lag Putting","cancha":can2,"resultado":res2}
                requests.post(URL, json=js)
                st.success("¡Registrado!")

else:
    st.header("📊 Mis Estadísticas")
    # En móvil las columnas se apilan solas, pero forzamos el orden
    df1 = leer("Putt_Corto")
    if not df1.empty:
        st.subheader("🎯 Práctica Corto")
        res = df1.groupby('Subcategoria').agg({'Aciertos':'sum','Intentos':'sum'}).reset_index()
        res['%'] = (res['Aciertos']/res['Intentos'])*100
        st.plotly_chart(px.bar(res, x='Subcategoria', y='%', range_y=[0,105], text='%'), use_container_width=True)
    
    df2 = leer("Lag_Putting")
    if not df2.empty:
        st.subheader("📏 Práctica Lag")
        cols = ["Menos De 1 Metro", "Entre Un Metro Y Un Metro Y Medio", "Mas De Un Metro Y Medio"]
        existentes = [c for c in cols if c in df2.columns]
        if existentes:
            vals = [df2[c].sum() for c in existentes]
            st.plotly_chart(px.pie(values=vals, names=existentes, hole=0.4), use_container_width=True)
