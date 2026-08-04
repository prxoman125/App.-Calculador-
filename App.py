import streamlit as st
import time

st.set_page_config(page_title="Reto de Preguntas", layout="centered")

# Estilo para botones grandes y textos visibles en video
st.markdown("""
    <style>
    .big-text { font-size:24px !important; font-weight: bold; text-align: center; }
    .question-text { font-size:32px !important; font-weight: bold; color: #1E88E5; text-align: center; }
    .timer-text { font-size:60px !important; font-weight: bold; color: #E53935; text-align: center; }
    </style>
""", unsafe_allow_html=True) # <-- AQUÍ SE CORRIGIÓ EL PARÁMETRO

st.title("🔔 Control de Retos - Cultura General")

# Base de datos simple de preguntas
preguntas = [
    {"p": "¿Cuántos lados tiene un hexágono?", "r": "6 lados"},
    {"p": "¿Cuál es el tercer planeta del sistema solar?", "r": "La Tierra"},
    {"p": "¿Qué año se descubrió América?", "r": "1492"}
]

# Estado de la app
if 'num_pregunta' not in st.session_state:
    st.session_state.num_pregunta = 0

# Mostrar pregunta actual
idx = st.session_state.num_pregunta % len(preguntas)
st.markdown(f"<p class='question-text'>{preguntas[idx]['p']}</p>", unsafe_allow_html=True)

# Contenedor para el temporizador
timer_placeholder = st.empty()

# Botones de control del juego
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⏱️ Iniciar Tiempo", use_container_width=True):
        # Cuenta regresiva de 10 segundos
        for segundos in range(10, -1, -1):
            timer_placeholder.markdown(f"<p class='timer-text'>{segundos}s</p>", unsafe_allow_html=True)
            time.sleep(1)
        timer_placeholder.markdown("<p class='timer-text'>❌ ¡TIEMPO! Al fondo de la fila</p>", unsafe_allow_html=True)

with col2:
    if st.button("✅ ¡Acierto / Premio!", use_container_width=True):
        timer_placeholder.markdown("<p class='big-text' style='color:green;'>🎉 ¡RESPUESTA CORRECTA!</p>", unsafe_allow_html=True)

with col3:
    if st.button("➡️ Siguiente Pareja", use_container_width=True):
        st.session_state.num_pregunta += 1
        st.rerun()

# Acordeón oculto para el creador
with st.expander("👁️ Ver Respuesta Correcta (Solo para el creador)"):
    st.write(preguntas[idx]['r'])
