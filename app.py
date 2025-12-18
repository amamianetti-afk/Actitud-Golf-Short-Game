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
        else:
            cancha = st.text_input("Cancha:")
            hoyo = st.number_input("Hoyo:", 1, 18, 1)
            res_c = st.selectbox("Resultado:", ["Emboqué", "Falle: Corta en linea", "Falle: Corta derecha", "Falle: Corta izquierda", "Falle: Larga en linea", "Falle: Larga derecha", "Falle: Larga izquierda"])
            rut = st.radio("¿Rutina?", ["Sí", "No"])
            if st.button("Guardar Putt Cancha"):
                datos = {"fecha": str(fecha), "entorno": modo, "tipo": "Putt Corto", "cancha": cancha, "hoyo": hoyo, "resultado": res_c, "rutina": rut}
                requests.post(URL_WEB_APP, json=datos)
                st.success("¡Registrado!")

    with tab2:
        if modo == "Práctica":
            rango = st.selectbox("Rango:", ["Lag A (2.5-8m)", "Lag B (8.5-15m)", "Lag C (15.5-25m)"])
            col1, col2, col3 = st.columns(3)
            cerca = col1.number_input("< 1m", 0, 10, 0)
            media = col2.number_input("1m a 1.5m", 0, 10, 0)
            lejos = col3.number_input("> 1.5m", 0, 10, 0)
            if st.button("Guardar Práctica Lag") and (cerca+media+lejos==10):
                datos = {"fecha": str(fecha), "entorno": modo, "tipo": "Lag Putting", "subcategoria": rango, "cerca": cerca, "media": media, "lejos": lejos}
                requests.post(URL_WEB_APP, json=datos)
                st.success("¡Guardado!")
        else:
            cancha_l = st.text_input("Cancha:", key="cl")
            dist_l = st.number_input("Metros:", 1.0, 50.0, 10.0)
            res_l = st.selectbox("Resultado:", ["Emboqué", "a 50cm", "a 1m", "a 1.5m", "más de 1.5m"])
            if st.button("Guardar Lag Cancha"):
                datos = {"fecha": str(fecha), "entorno": modo, "tipo": "Lag Putting", "cancha": cancha_l, "distancia": dist_l, "resultado": res_l}
                requests.post(URL_WEB_APP, json=datos)
                st.success("¡Registrado!")

else: # SECCIÓN DE ESTADÍSTICAS
    st.header("📊 Análisis de Rendimiento")
    
    try:
        # 1. Putt Corto Práctica (CORREGIDO PARA MOSTRAR 100%)
        df_pc = leer_hoja("Putt_Corto")
        if not df_pc.empty:
            st.subheader("🎯 Efectividad Putt Corto (Práctica)")
            
            # Agrupamos por distancia y sumamos aciertos e intentos totales
            df_resumen = df_pc.groupby('Subcategorìa').agg({
                'Aciertos': 'sum',
                'Intentos': 'sum'
            }).reset_index()
            
            # Calculamos el % real sobre el total
            df_resumen['% Efectividad'] = (df_resumen['Aciertos'] / df_resumen['Intentos']) * 100
            
            # Creamos el gráfico con el nuevo %
            fig = px.bar(
                df_resumen, 
                x='Subcategorìa', 
                y='% Efectividad', 
                color='Subcategorìa',
                range_y=[0, 100],  # Forzamos que el eje llegue a 100
                text=df_resumen['% Efectividad'].apply(lambda x: f'{x:.1f}%'), # Muestra el número arriba
                title="Promedio de Efectividad por Distancia"
            )
            st.plotly_chart(fig)

        # 2. Lag Putting Práctica
        df_lp = leer_hoja("Lag_Putting")
        if not df_lp.empty:
            st.subheader("📏 Distribución Lag Putting")
            # Sumamos totales de cerca, media y lejos
            totales = [df_lp['Cerca'].sum(), df_lp['Media'].sum(), df_lp['Lejos'].sum()]
            nombres = ['< 1m', '1m a 1.5m', '> 1.5m']
            fig2 = px.pie(values=totales, names=nombres, title="Control de Distancia Total")
            st.plotly_chart(fig2)
            
        # 3. Errores en Cancha (Putt Corto)
        df_pcc = leer_hoja("Putt_Corto_Cancha")
        if not df_pcc.empty:
            st.subheader("🚩 Tendencia de Fallos en Cancha")
            fallos = df_pcc[df_pcc['Resultado'] != "Emboqué"]
            if not fallos.empty:
                fig3 = px.histogram(fallos, x='Resultado', title="¿Cómo estás fallando?")
                st.plotly_chart(fig3)
            else:
                st.info("¡Todavía no tienes fallos registrados en cancha! (Buen trabajo)")

    except:
        st.warning("Carga más datos para ver las estadísticas.")
