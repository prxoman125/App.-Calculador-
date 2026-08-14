import streamlit as st

# Configuración de la página para móviles
st.set_page_config(page_title="Agenda Médica", layout="centered")

st.title("🏥 Control Médico")
st.subheader("Registro de Pacientes")

# Formulario para el consultorio
nombre = st.text_input("Nombre completo del paciente:")
edad = st.number_input("Edad:", min_value=0, max_value=120, step=1)
motivo = st.text_area("Motivo de la consulta:")

if st.button("Guardar Registro"):
    if nombre and motivo:
        st.success(f"¡Paciente {nombre} registrado con éxito!")
        # Aquí puedes agregar lógica para guardar los datos
    else:
        st.error("Por favor llena todos los campos.")
