import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Actitud Golf Pro", page_icon="⛳")

# URL de tu Apps Script actualizada
URL_WEB_APP = "https://script.google.com/macros/s/AKfycbyaJoEhqBcyelhlK5fjnbl70lA6Jwaq0wDxIKL7CMmYeO6MQUGfy8Ubhu0LC9Ri9sy4/exec"

st.title("⛳ Actitud Golf - Tracker")

with st.sidebar:
    st.header("Configuración")
    modo = st.radio("Entorno:", ["Práctica", "Juego en Cancha"])
    fecha = st.date_input("Fecha", datetime.now())

tab1, tab2 = st.tabs(["🎯 Putt Corto", "📏 Lag Putting"])

with tab1:
    st.subheader("🎯 Sesión de Putt Corto")
    dist = st.selectbox("Distancia:", ["35cm", "70cm", "1m", "1.5m", "2m"])
    c1, c2 = st.columns(2)
    intentos = c1.number_input("Intentos", 1, 100, 10)
    aciertos = c2.number_input("Aciertos", 0, intentos, 0)
    
    if st.button("Guardar Putt Corto"):
        datos = {"fecha": str(fecha), "entorno": modo, "tipo": "Putt Corto", "subcategoria": dist, "intentos": intentos, "aciertos": aciertos}
        res = requests.post(URL_WEB_APP, json=datos)
        if res.status_code == 200:
            st.success("¡Datos guardados!")
            st.balloons()

with tab2:
    if modo == "Práctica":
        st.subheader("📏 Lag Putting: Entrenamiento")
        rango = st.selectbox("Rango:", ["Lag A (2.5-8m)", "Lag B (8.5-15m)", "Lag C (15.5-25m)"])
        st.write("De 10 bolas, ¿dónde quedaron?")
        col1, col2, col3 = st.columns(3)
        cerca = col1.number_input("< 1m", 0, 10, 0)
        media = col2.number_input("1m a 1.5m", 0, 10, 0)
        lejos = col3.number_input("> 1.5m", 0, 10, 0)
        
        suma = cerca + media + lejos
        if suma == 10:
            if st.button("Guardar Práctica"):
                datos = {"fecha": str(fecha), "entorno": modo, "tipo": "Lag Putting", "subcategoria": rango, "cerca": cerca, "media": media, "lejos": lejos}
                requests.post(URL_WEB_APP, json=datos)
                st.success("¡Práctica registrada!")
                st.balloons()
        else:
            st.warning(f"La suma actual es {suma}. Debe ser 10.")

    else: # MODO JUEGO EN CANCHA
        st.subheader("🏌️ Registro de Golpe Real")
        cancha = st.text_input("Cancha:", placeholder="Ej: Olivos Golf")
        hoyo = st.number_input("Hoyo:", 1, 18, 1)
        dist_m = st.number_input("Distancia al hoyo (metros):", 1.0, 50.0, 10.0)
        
        resultado = st.selectbox("Resultado:", [
            "Emboqué", 
            "a 50cm o menos", 
            "a 1 metro o menos", 
            "a 1.5 metros o menos", 
            "a más de 1.5 metros"
        ])
        
        col_r, col_f = st.columns(2)
        rutina = col_r.radio("¿Seguí mi rutina?", ["Sí", "No"])
        foco = col_f.radio("¿Foco en ejecución?", ["Sí", "No"])
        
        comentarios = st.text_area("Comentarios (puedes dictar con el teclado de tu cel):")
        
        if st.button("Guardar Golpe Real"):
            datos = {
                "fecha": str(fecha), 
                "entorno": modo, 
                "tipo": "Lag Putting",
                "cancha": cancha, 
                "hoyo": hoyo, 
                "distancia": dist_m,
                "resultado": resultado, 
                "rutina": rutina, 
                "foco": foco,
                "comentarios": comentarios
            }
            res = requests.post(URL_WEB_APP, json=datos)
            if res.status_code == 200:
                st.success("¡Hoyo registrado con éxito en la planilla!")
                st.balloons()
