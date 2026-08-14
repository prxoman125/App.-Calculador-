import streamlit as st

st.title("Calculadora de Capítulos y Copias (USD a MXN)")
st.write("Configura el costo por capítulo, las copias vendidas de cada uno y obtén el reparto.")

# Configuración del Tipo de Cambio en la barra lateral
st.sidebar.header("Tipo de Cambio")
tipo_cambio = st.sidebar.number_input("1 USD a MXN:", min_value=1.0, value=17.03, step=0.01)

st.markdown("---")
st.subheader("1. Disponibilidad de Capítulos")

# Entrada para la cantidad de capítulos
cantidad_capitulos = st.number_input("Ingresa la cantidad de capítulos totales:", min_value=0, value=3, step=1)

st.markdown("---")
st.subheader("2. Datos de Costos y Ventas")

# Entrada del precio base por capítulo
precio_por_capitulo_usd = st.number_input("Precio por capítulo (USD $):", min_value=0.0, value=50.0, step=5.0)

# Diccionario o lista para guardar las copias de cada capítulo
copias_por_capitulo = {}
total_copias_vendidas = 0

# Generar entradas dinámicas según la cantidad de capítulos
if cantidad_capitulos > 0:
    st.markdown("#### Copias vendidas por capítulo:")
    # Usamos columnas para que no ocupe tanto espacio vertical si son muchos capítulos
    cols = st.columns(min(cantidad_capitulos, 3)) 
    
    for i in range(cantidad_capitulos):
        num_capitulo = i + 1
        # Distribuir los inputs entre las columnas creadas
        with cols[i % 3]:
            copias = st.number_input(
                f"Copias del Cap. {num_capitulo}:", 
                min_value=0, 
                value=1, 
                step=1, 
                key=f"cap_{num_capitulo}"
            )
            copias_por_capitulo[num_capitulo] = copias
            total_copias_vendidas += copias

# Cálculos económicos basados en el total de copias vendidas
total_produccion_usd = precio_por_capitulo_usd * total_copias_vendidas
total_produccion_mxn = total_produccion_usd * tipo_cambio

st.markdown("---")
st.subheader("3. Resultado Total de las Ventas")
st.write(f"Total de copias vendidas entre todos los capítulos: **{total_copias_vendidas} copias**")

col_t1, col_t2 = st.columns(2)
with col_t1:
    st.metric(label="Total General (USD)", value=f"${total_produccion_usd:,.2f} USD")
with col_t2:
    st.metric(label="Total General (MXN)", value=f"${total_produccion_mxn:,.2f} MXN")

st.markdown("---")
st.subheader("4. Configuración de Porcentajes de Reparto")

# Deslizador para Jeremy con incrementos de 0.5 en 0.5
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
