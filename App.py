import streamlit as st

st.title("Ustatic de Cámara Móvil")
imagen = st.camera_input("Toma una foto")

if imagen is not None:
  st.success("¡Foto capturada con éxito!")
  st.image(imagen)
