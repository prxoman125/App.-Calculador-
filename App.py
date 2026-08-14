import streamlit as st

st.title("Calculadora de Ventas y Reparto")
st.write("Ingresa los datos del producto y ajusta los porcentajes de ganancias.")

# Entradas principales del producto
precio_unitario = st.number_input("Precio original por producto ($):", min_value=0.0, value=100.0, step=5.0)
cantidad_vendida = st.number_input("Cantidad de productos vendidos:", min_value=0, value=10, step=1)

# Cálculo del total
total_venta = precio_unitario * cantidad_vendida
st.subheader(f"Total de la Venta: ${total_venta:,.2f}")

st.markdown("---")
st.subheader("Configuración de Porcentajes de Reparto")

# Porcentaje para Jeremy (el de José Luis se calcula automáticamente para sumar 100%)
porcentaje_jeremy = st.slider("Porcentaje para Jeremy (%):", min_value=0, max_value=100, value=50)
porcentaje_jose = 100 - porcentaje_jeremy

st.write(f"Porcentaje para José Luis (%): **{porcentaje_jose}%**")

# Validación visual para asegurar que sumen 100%
if porcentaje_jeremy + porcentaje_jose != 100:
    st.error("Los porcentajes deben sumar exactamente 100%.")
else:
    # Montos correspondientes
    monto_jeremy = total_venta * (porcentaje_jeremy / 100)
    monto_jose = total_venta * (porcentaje_jose / 100)

    st.markdown("---")
    st.subheader("Resultados del Reparto")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Le toca a Jeremy", value=f"${monto_jeremy:,.2f}", delta=f"{porcentaje_jeremy}%")
    with col2:
        st.metric(label="Le toca a José Luis", value=f"${monto_jose:,.2f}", delta=f"{porcentaje_jose}%")
