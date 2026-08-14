import streamlit as st

st.title("Calculadora de Capítulos (USD a MXN)")
st.write("Configura el costo por capítulo en dólares y obtén el desglose en pesos.")

# Configuración del Tipo de Cambio en la barra lateral
st.sidebar.header("Tipo de Cambio")
tipo_cambio = st.sidebar.number_input("1 USD a MXN:", min_value=1.0, value=17.03, step=0.01)

st.markdown("---")
st.subheader("Datos de la Producción / Capítulos")

# Entradas adaptadas a capítulos (ingreso en USD)
precio_por_capitulo_usd = st.number_input("Precio por capítulo (USD $):", min_value=0.0, value=50.0, step=5.0)
cantidad_capitulos = st.number_input("Cantidad de capítulos:", min_value=0, value=5, step=1)

# Cálculos económicos en dólares y conversión a moneda nacional
total_produccion_usd = precio_por_capitulo_usd * cantidad_capitulos
total_produccion_mxn = total_produccion_usd * tipo_cambio

# Despliegue de los totales generales
col_t1, col_t2 = st.columns(2)
with col_t1:
    st.metric(label="Total en Dólares (USD)", value=f"${total_produccion_usd:,.2f} USD")
with col_t2:
    st.metric(label="Total en Pesos (MXN)", value=f"${total_produccion_mxn:,.2f} MXN")

st.markdown("---")
st.subheader("Configuración de Porcentajes de Reparto")

# Deslizador para Jeremy con incrementos estrictos de 0.5 en 0.5
porcentaje_jeremy = st.slider(
    "Porcentaje para Jeremy (%):", 
    min_value=0.0, 
    max_value=100.0, 
    value=50.0, 
    step=0.5
)
porcentaje_jose = 100.0 - porcentaje_jeremy

st.write(f"Porcentaje para José Luis (%): **{porcentaje_jose:.1f}%**")

# Reparto matemático final convertido a MXN
monto_jeremy_mxn = total_produccion_mxn * (porcentaje_jeremy / 100)
monto_jose_mxn = total_produccion_mxn * (porcentaje_jose / 100)

st.markdown("---")
st.subheader("Resultados del Reparto (en Pesos Mexicanos MXN)")

# Mapeo visual de ganancias individuales
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Le toca a Jeremy", value=f"${monto_jeremy_mxn:,.2f} MXN", delta=f"{porcentaje_jeremy}%")
with col2:
    st.metric(label="Le toca a José Luis", value=f"${monto_jose_mxn:,.2f} MXN", delta=f"{porcentaje_jose}%")
