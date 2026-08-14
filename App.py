import streamlit as st

st.title("Calculadora de Ventas (USD a MXN)")
st.write("Ingresa los datos en dólares y obtén el reparto en pesos mexicanos.")

# Configuración del Tipo de Cambio
st.sidebar.header("Tipo de Cambio")
tipo_cambio = st.sidebar.number_input("1 USD a MXN:", min_value=1.0, value=17.03, step=0.01)

st.markdown("---")
st.subheader("Datos de la Venta (en USD)")

# Entradas principales del producto en USD
precio_unitario_usd = st.number_input("Precio por producto (USD $):", min_value=0.0, value=10.0, step=1.0)
cantidad_vendida = st.number_input("Cantidad de productos vendidos:", min_value=0, value=10, step=1)

# Cálculos intermedios en USD y conversión a MXN
total_venta_usd = precio_unitario_usd * cantidad_vendida
total_venta_mxn = total_venta_usd * tipo_cambio

# Mostrar totales en la app
col_t1, col_t2 = st.columns(2)
with col_t1:
    st.metric(label="Total Venta (USD)", value=f"${total_venta_usd:,.2f} USD")
with col_t2:
    st.metric(label="Total Venta (MXN)", value=f"${total_venta_mxn:,.2f} MXN")

st.markdown("---")
st.subheader("Configuración de Porcentajes de Reparto")

# Porcentaje para Jeremy con saltos de 0.5 en 0.5
porcentaje_jeremy = st.slider(
    "Porcentaje para Jeremy (%):", 
    min_value=0.0, 
    max_value=100.0, 
    value=50.0, 
    step=0.5
)
porcentaje_jose = 100.0 - porcentaje_jeremy

st.write(f"Porcentaje para José Luis (%): **{porcentaje_jose:.1f}%**")

# Montos correspondientes ya transformados a Pesos Mexicanos (MXN)
monto_jeremy_mxn = total_venta_mxn * (porcentaje_jeremy / 100)
monto_jose_mxn = total_venta_mxn * (porcentaje_jose / 100)

st.markdown("---")
st.subheader("Resultados del Reparto (en Pesos Mexicanos MXN)")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Le toca a Jeremy", value=f"${monto_jeremy_mxn:,.2f} MXN", delta=f"{porcentaje_jeremy}%")
with col2:
    st.metric(label="Le toca a José Luis", value=f"${monto_jose_mxn:,.2f} MXN", delta=f"{porcentaje_jose}%")
