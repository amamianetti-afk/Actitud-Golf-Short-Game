import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Actitud Golf Pro", page_icon="⛳", layout="wide")

# CONFIGURACIÓN
URL_WEB_APP = "https://script.google.com/macros/s/AKfycbzkhoD7Zxucrjoi29aCH7xGFykud7XotbOEvSJUgVc_GBjG7LbnIwfriNVNvUOU_Nrc/exec"
SHEET_ID = "1p3vWVzoHAgMk4bHY6OL3tnQLPhclGqcYspkwTw0AjFU"

# --- DEFINICIÓN DE NOMBRES DE COLUMNAS PARA LAG PUTTING ---
COL_LAG_1 = "menos de 1 metro"
COL_LAG_2 = "entre un metro y un metro y medio" # <-- ESTE ES EL CAMBIO
COL_LAG_3 = "mas de un metro y medio"

def leer_hoja(sheet_name):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

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
            if st.button("Guardar Putt Cancha"):
                datos = {"fecha": str(fecha), "entorno": modo, "tipo": "Putt Corto", "cancha": cancha, "hoyo": hoyo, "distancia": dist_c, "resultado": res_c, "rutina": "Sí", "foco": "Sí"}
                requests.post(URL_WEB_APP, json=datos)
                st.success("¡Registrado!")

    with tab2:
        if modo == "Práctica":
            rango = st.selectbox("Rango:", ["Lag A (2.5-8m)", "Lag B (8.5-15m)", "Lag C (15.5-25m)"])
            col1, col2, col3 = st.columns(3)
            
            v1 = col1.number_input(COL_LAG_1, 0, 10, 0)
            v2 = col2.number_input(COL_LAG_2, 0, 10, 0)
            v3 = col3.number_input(COL_LAG_3, 0, 10, 0)
            
            if st.button("Guardar Práctica Lag"):
                if (v1 + v2 + v3 == 10):
                    datos = {
                        "fecha": str(fecha), "entorno": modo, "tipo": "Lag Putting", "subcategoria": rango,
                        COL_LAG_1: v1, COL_LAG_2: v2, COL_LAG_3: v3
                    }
                    res = requests.post(URL_WEB_APP, json=datos)
                    st.success("¡Sesión de Lag Guardada!")
                    st.balloons()
                else:
                    st.error("La suma debe ser 10")
        else:
            cancha_l = st.text_input("Cancha:", key="cl")
            dist_l = st.number_input("Metros al hoyo:", 1.0, 50.0, 10.0)
            res_l = st.selectbox("Resultado:", ["Emboqué", "a 50cm", "a 1m", "a 1.5m", "más de 1.5m"])
            if st.button("Guardar Lag Cancha"):
                datos = {"fecha": str(fecha), "entorno": modo, "tipo": "Lag Putting", "cancha": cancha_l, "distancia": dist_l, "resultado": res_l}
                requests.post(URL_WEB_APP, json=datos)
                st.success("¡Registrado!")

else: # ESTADÍSTICAS
    st.header("📊 Análisis de Rendimiento")
    
    # 1. Putt Corto
    df_pc = leer_hoja("Putt_Corto")
    if not df_pc.empty:
        st.subheader("🎯 Efectividad Putt Corto (Práctica)")
        df_pc.columns = [c.replace('Subcategorìa', 'Subcategoria') for c in df_pc.columns]
        if 'Subcategoria' in df_pc.columns:
            df_resumen = df_pc.groupby('Subcategoria').agg({'Aciertos': 'sum', 'Intentos': 'sum'}).reset_index()
            df_resumen['%'] = (df_resumen['Aciertos'] / df_resumen['Intentos']) * 100
            orden = ["35cm", "70cm", "1m", "1.5m", "2m"]
            df_resumen['Subcategoria'] = pd.Categorical(df_resumen['Subcategoria'], categories=orden, ordered=True)
            fig = px.bar(df_resumen.sort_values('Subcategoria'), x='Subcategoria', y='%', range_y=[0,105], 
                         text=df_resumen['%'].apply(lambda x: f'{x:.1f}%'), color='Subcategoria')
            st.plotly_chart(fig)

    # 2. Lag Putting
    df_lp = leer_hoja("Lag_Putting")
    if not df_lp.empty:
        st.subheader("📏 Distribución Lag Putting (Práctica)")
        
        # Usamos las variables de nombre que definimos arriba
        for col in [COL_LAG_1, COL_LAG_2, COL_LAG_3]:
            if col in df_lp.columns:
                df_lp[col] = pd.to_numeric(df_lp[col], errors='coerce').fillna(0)
        
        s1 = df_lp[COL_LAG_1].sum() if COL_LAG_1 in df_lp.columns else 0
        s2 = df_lp[COL_LAG_2].sum() if COL_LAG_2 in df_lp.columns else 0
        s3 = df_lp[COL_LAG_3].sum() if COL_LAG_3 in df_lp.columns else 0
        
        if (s1 + s2 + s3) > 0:
            fig2 = px.pie(values=[s1, s2, s3], names=[COL_LAG_1, COL_LAG_2, COL_LAG_3], hole=0.4)
            st.plotly_chart(fig2)
        else:
            st.info("Aún no hay datos de Lag cargados.")
