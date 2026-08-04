import streamlit as st
st.set_page_config(page_title="Calculadora por Sectores", layout="centered")
st.markdown("""
    <style>
    #MainMenu, header, footer { visibility: hidden !important; }
    .titulo-container {
        background: linear-gradient(135deg, #020617 0%, #020A18 25%, #060214 50%, #0A0218 75%, #020617 100%);
        background-size: 400% 400%;
        animation: fondoAzulMorado 10s ease-in-out infinite;
        padding: 24px; border-radius: 12px; text-align: center; margin-bottom: 28px; border: 2px solid #0F172A;
    }
    .titulo-texto {
        background: linear-gradient(to right, #3B82F6, #06B6D4, #8B5CF6, #EC4899, #3B82F6);
        background-size: 300% auto;
        -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
        background-clip: text !important; animation: brilloLetrasAnimacion 8s linear infinite;
        font-family: 'Inter', sans-serif; font-weight: 700; font-size: 30px; margin: 0 !important; display: inline-block;
    }
    @keyframes brilloLetrasAnimacion { 0% { background-position: 0% center; } 100% { background-position: 300% center; } }
    @keyframes fondoAzulMorado {
        0% { background-position: 0% 50%; border-color: #0F172A; box-shadow: 0 0 12px rgba(15, 23, 42, 0.8); }
        50% { background-position: 100% 50%; border-color: #1A1033; box-shadow: 0 0 12px rgba(26, 16, 51, 0.8); }
        100% { background-position: 0% 50%; border-color: #0F172A; box-shadow: 0 0 12px rgba(15, 23, 42, 0.8); }
    }
    div[data-testid="stNotificationV2"], div[role="alert"], div.stAlert { background-image: none !important; background-color: transparent !important; border-radius: 8px !important; }
    div[data-testid="stNotificationV2"]:has(svg[title="Success"]), div[role="alert"]:has(svg[title="Success"]), .stAlert:has(svg[title="Success"]) {
        background: linear-gradient(135deg, #10B981, #064E3B) !important; border: 2px solid #10B981 !important; color: #FFFFFF !important;
    }
    div[data-testid="stNotificationV2"]:has(svg[title="Info"]), div[role="alert"]:has(svg[title="Info"]), .stAlert:has(svg[title="Info"]) {
        background: linear-gradient(135deg, #3B82F6, #1E3A8A) !important; border: 2px solid #3B82F6 !important; color: #FFFFFF !important;
    }
    .stAlert p, .stAlert div, div[role="alert"] p, div[data-testid="stNotificationContent"] span { color: #FFFFFF !important; }
    div[data-testid="stNumberInput"] > div:first-of-type, div[data-testid="stSelectbox"] > div:first-of-type > div {
        border: 2px solid #1A365D !important; border-radius: 8px !important; background: linear-gradient(135deg, #22252A, #0F1115) !important;
    }
    .stNumberInput input { color: #FFFFFF !important; text-align: center !important; padding-left: 80px !important; padding-right: 90px !important; }
    </style>
""", unsafe_allow_html=True)
st.markdown('<div class="titulo-container"><span class="titulo-texto">Calculadora Interactiva por Sectores</span></div>', unsafe_allow_html=True)
st.write("Selecciona un sector, ingresa los datos y calcula los resultados de forma automática.")
sector = st.selectbox("Elige el sector económico:", ["Tecnología / Software", "Manufactura", "Comercio / Retail"])
st.divider()
if sector == "Tecnología / Software":
    st.subheader("💻 Sector Tecnológico")
    usuarios = st.number_input("Número de usuarios activos:", min_value=1, value=50, step=1)
    costo_por_usuario = st.number_input("Costo mensual por usuario ($):", min_value=0.0, value=15.0, step=0.5)
    descuento = st.number_input("Descuento aplicado (%):", min_value=0, max_value=100, value=5, step=1)
    if st.button("Calcular Total"):
        st.success(f"Costo Total Mensual: ${(usuarios * costo_por_usuario * (1 - descuento / 100)):.2f}")
elif sector == "Manufactura":
    st.subheader("⚙️ Sector Manufactura")
    unidades = st.number_input("Unidades a producir:", min_value=1, value=1000, step=10)
    costo_material = st.number_input("Costo de material por unidad ($):", min_value=0.0, value=5.5, step=0.1)
    costo_operativo_fijo = st.number_input("Costos operativos fijos ($):", min_value=0.0, value=2000.0, step=50.0)
    if st.button("Calcular Costo de Producción"):
        total = (unidades * costo_material) + costo_operativo_fijo
        st.success(f"Costo Total: ${total:.2f}"); st.info(f"Costo por unidad: ${total/unidades:.2f}")
elif sector == "Comercio / Retail":
    st.subheader("🛍️ Sector Comercio")
    costo_producto = st.number_input("Costo de adquisición ($):", min_value=0.0, value=50.0, step=1.0)
    margen_ganancia = st.number_input("Margen de ganancia (%):", min_value=1, max_value=500, value=30, step=5)
    impuesto = st.number_input("IVA (%):", min_value=0.0, value=16.0, step=0.5)
    if st.button("Calcular Precio de Venta"):
        precio_final = costo_producto * (1 + margen_ganancia / 100) * (1 + impuesto / 100)
        st.success(f"Precio Venta: ${precio_final:.2f}"); st.info(f"Ganancia: ${precio_final - costo_producto:.2f}")
