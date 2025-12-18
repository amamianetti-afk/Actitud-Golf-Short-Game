import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Actitud Golf Master", page_icon="⛳")

# URL de tu Apps Script (Actualizada)
URL_WEB_APP = "https://script.google.com/macros/s/AKfycbwT40gujHrmqKIgDe5ckyNLCdW8CK5Cv2BF5E0eT0Hspr-vpyMSNbxiqyFoVSFVs-Ka/exec"

st.title("⛳ Actitud Golf - Tracker")

with st.sidebar:
    st.header("Configuración")
    modo = st.radio("Entorno:", ["Práctica", "Juego en Cancha"])
    fecha = st.date_input("Fecha", datetime.now())

tab1, tab2 = st.tabs(["🎯 Putt Corto", "📏 Lag Putting"])

# --- PESTAÑA 1: PUTT CORTO ---
with tab1:
    st.subheader("🎯 Control de Putt Corto")
    if modo == "Práctica":
        dist = st.selectbox("Distancia de práctica:", ["35cm", "70cm", "1m", "1.5m", "2m"])
        c1, c2 = st.columns(2)
        intentos = c1.number_input("Intentos", 1, 100, 10)
        aciertos = c2.number_input("Aciertos", 0, intentos, 0)
        if st.button("Guardar Práctica Corto"):
            datos = {"fecha": str(fecha), "entorno": modo, "tipo": "Putt Corto", "subcategoria": dist, "intentos": intentos, "aciertos": aciertos}
            requests.post(URL_WEB_APP, json=datos)
            st.success("¡Práctica de Putt Corto guardada!")
            st.balloons()
    else:
        st.write("🏃 Registro de Putt Corto en Cancha")
        cancha = st.text_input("Cancha:", key="c_c")
        hoyo = st.number_input("Hoyo:", 1, 18, 1, key="h_c")
        dist_c = st.selectbox("Distancia aprox:", ["35cm", "70cm", "1m", "1.5m", "2m", "Más"])
        
        res_c = st.selectbox("Resultado:", [
            "Emboqué", 
            "Falle: Corta en linea", "Falle: Corta derecha", "Falle: Corta izquierda",
            "Falle: Larga en linea", "Falle: Larga derecha", "Falle: Larga izquierda"
        ])
        
        c1, c2 = st.columns(2)
        rut = c1.radio("¿Seguí mi rutina?", ["Sí", "No"], key="r_c")
        foc = c2.radio("¿Foco en ejecución?", ["Sí", "No"], key="f_c")
        com = st.text_area("Comentarios / Notas:", key="n_c")
        
        if st.button("Guardar Putt Cancha"):
            datos = {
                "fecha": str(fecha), "entorno": modo, "tipo": "Putt Corto",
                "cancha": cancha, "hoyo": hoyo, "distancia": dist_c,
                "resultado": res_c, "rutina": rut, "foco": foc, "comentarios": com
            }
            res = requests.post(URL_WEB_APP, json=datos)
            if res.status_code == 200:
                st.success("¡Hoyo registrado en Putt_Corto_Cancha!")
                st.balloons()

# --- PESTAÑA 2: LAG PUTTING ---
with tab2:
    st.subheader("📏 Control de Lag Putting")
    if modo == "Práctica":
        rango = st.selectbox("Rango de Práctica:", ["Lag A (2.5-8m)", "Lag B (8.5-15m)", "Lag C (15.5-25m)"])
        st.write("De 10 bolas, ¿dónde quedaron?")
        col1, col2, col3 = st.columns(3)
        cerca = col1.number_input("< 1m", 0, 10, 0)
        media = col2.number_input("1m a 1.5m", 0, 10, 0)
        lejos = col3.number_input("> 1.5m", 0, 10, 0)
        
        if (cerca + media + lejos) == 10:
            if st.button("Guardar Práctica Lag"):
                datos = {"fecha": str(fecha), "entorno": modo, "tipo": "Lag Putting", "subcategoria": rango, "cerca": cerca, "media": media, "lejos": lejos}
                requests.post(URL_WEB_APP, json=datos)
                st.success("¡Sesión de Lag guardada!")
                st.balloons()
        else:
            st.warning(f"La suma es {cerca+media+lejos}. Debe ser exactamente 10.")
    else:
        st.write("🏌️ Registro de Lag en Cancha")
        cancha_l = st.text_input("Cancha:", key="c_l")
        hoyo_l = st.number_input("Hoyo:", 1, 18, 1, key="h_l")
        dist_l = st.number_input("Metros al hoyo:", 1.0, 50.0, 10.0)
        res_l = st.selectbox("Resultado:", ["Emboqué", "a 50cm o menos", "a 1 metro o menos", "a 1.5 metros o menos", "a más de 1.5 metros"])
        
        c1l, c2l = st.columns(2)
        rut_l = c1l.radio("¿Seguí mi rutina?", ["Sí", "No"], key="r_l")
        foc_l = c2l.radio("¿Foco en ejecución?", ["Sí", "No"], key="f_l")
        com_l = st.text_area("Comentarios / Notas:", key="n_l")
        
        if st.button("Guardar Lag Cancha"):
            datos = {
                "fecha": str(fecha), "entorno": modo, "tipo": "Lag Putting",
                "cancha": cancha_l, "hoyo": hoyo_l, "distancia": dist_l,
                "resultado": res_l, "rutina": rut_l, "foco": foc_l, "comentarios": com_l
            }
            res = requests.post(URL_WEB_APP, json=datos)
            if res.status_code == 200:
                st.success("¡Hoyo registrado en Lag_Cancha!")
                st.balloons()
