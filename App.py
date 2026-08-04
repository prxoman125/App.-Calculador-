import streamlit as st

# Configuración de página e inyección de CSS con máxima especificidad
st.set_page_config(page_title="Calculadora por Sectores", layout="centered")

st.markdown("""
    <style>
    /* Ocultar el menú superior (Share, GitHub, etc.) y el pie de página */
    #MainMenu, header, footer {
        visibility: hidden !important;
    }
    
    /* === BANNER DEL TÍTULO - FONDO AZUL OSCURO A MORADO === */
    .titulo-container {
        /* Gradiente ultra oscuro para no tapar las letras, pero con movimiento visible */
        background: linear-gradient(135deg, #0A1930 0%, #1E3A8A 25%, #4C1D95 50%, #2E1065 75%, #0A1930 100%);
        background-size: 400% 400%;
        
        /* Animación lenta, sutil pero visible */
        animation: fondoAzulMorado 10s ease-in-out infinite;
        
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 28px;
        border: 2px solid #1E3A8A;
    }
    
    /* === LETRAS CON BRILLO === */
    .titulo-texto {
        background: linear-gradient(to right, #3B82F6, #06B6D4, #8B5CF6, #EC4899, #3B82F6);
        background-size: 300% auto;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        animation: brilloLetrasAnimacion 8s linear infinite;
        font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        font-size: 30px;
        letter-spacing: -0.5px;
        margin: 0 !important;
        padding: 0 !important;
        display: inline-block;
    }
    
    @keyframes brilloLetrasAnimacion {
        0% { background-position: 0% center; }
        100% { background-position: 300% center; }
    }
    
    /* === ANIMACIÓN NUEVA: AZUL OSCURO <-> MORADO OSCURO === */
    @keyframes fondoAzulMorado {
        0% {
            background-position: 0% 50%;
            border-color: #1E3A8A; /* Azul oscuro */
            box-shadow: 0 0 15px rgba(30, 58, 138, 0.5);
        }
        33% {
            background-position: 50% 50%;
            border-color: #4338CA; /* Intermedio azul-morado */
            box-shadow: 0 0 20px rgba(67, 56, 202, 0.6);
        }
        66% {
            background-position: 100% 50%;
            border-color: #4C1D95; /* Morado oscuro */
            box-shadow: 0 0 15px rgba(76, 29, 149, 0.5);
        }
        100% {
            background-position: 0% 50%;
            border-color: #1E3A8A; /* Regresa a azul oscuro */
            box-shadow: 0 0 15px rgba(30, 58, 138, 0.5);
        }
    }
    
    /* === CORRECCIÓN INTEGRAL DE LAS BARRAS DE RESULTADOS === */
    div[data-testid="stNotificationV2"], 
    div[role="alert"],
    div.stAlert,
    .element-container:has(div[role="alert"]) div[role="alert"] {
        background-image: none !important;
        background-color: transparent !important;
        border-radius: 8px !important;
    }
    div[data-testid="stNotificationV2"]:has(svg[title="Success"]),
    div[role="alert"]:has(svg[title="Success"]),
    .stAlert:has(svg[title="Success"]) {
        background: linear-gradient(135deg, #10B981, #064E3B) !important;
        border: 2px solid #10B981 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(6, 78, 59, 0.4) !important;
    }
    div[data-testid="stNotificationV2"]:has(svg[title="Info"]),
    div[role="alert"]:has(svg[title="Info"]),
    .stAlert:has(svg[title="Info"]) {
        background: linear-gradient(135deg, #3B82F6, #1E3A8A) !important;
        border: 2px solid #3B82F6 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.4) !important;
    }
    .stAlert p, .stAlert div, div[role="alert"] p, div[role="alert"] div, div[data-testid="stNotificationContent"] span {
        color: #FFFFFF !important;
    }
    div[data-testid="stNumberInput"] > div:first-of-type, 
    div[data-testid="stSelectbox"] > div:first-of-type > div {
        border: 2px solid #1A365D !important;
        border-radius: 8px !important;
        transition: all 0.25s ease-in-out !important;
        background: linear-gradient(135deg, #22252A, #0F1115) !important;
        position: relative !important;
    }
    div[data-testid="stNumberInput"] div, 
    div[data-testid="stSelectbox"] div {
        border: none !important;
        background-color: transparent !important;
    }
    .stNumberInput input {
        color: #FFFFFF !important;
        text-align: center !important;
        padding-left: 80px !important;
        padding-right: 90px !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        color: #FFFFFF !important;
    }
    div[data-testid="stNumberInput"] > div:first-of-type:hover,
    div[data-testid="stNumberInput"] > div:first-of-type:focus-within,
    div[data-testid="stSelectbox"] > div:first-of-type > div:hover,
    div[data-testid="stSelectbox"] > div:first-of-type > div:focus-within {
        border-color: #2B6CB0 !important;
        box-shadow: 0 0 12px rgba(43, 108, 176, 0.55) !important;
    }
    div[data-testid="stNumberInputStepUpAndDown"] {
        position: absolute !important;
        top: 0 !important;
        right: 12px !important;
        height: 100% !important;
        width: 80px !important;
        display: block !important;
        background: transparent !important;
    }
    button[data-testid="stNumberInputStepUp"], 
    button[data-testid="stNumberInputStepDown"] {
        position: absolute !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        height: 24px !important;
        width: 24px !important;
        margin: 0 !important;
        border-radius: 4px !important;
        border: none !important;
        color: #A0AEC0 !important;
        background-color: transparent !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    button[data-testid="stNumberInputStepDown"] { left: 6px !important; }
    button[data-testid="stNumberInputStepUp"] { right: 6px !important; }
    button[data-testid="stNumberInputStepUp"]:hover, 
    button[data-testid="stNumberInputStepDown"]:hover {
        color: #FFFFFF !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    button[data-testid="stNumberInputStepUp"]:active, 
    button[data-testid="stNumberInputStepDown"]:active {
        background-color: #1A365D !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 10px #1A365D, 0 0 20px #1A365D !important;
        transform: translateY(-50%) scale(0.92) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="titulo-container"><span class="titulo-texto">Calculadora Interactiva por Sectores</span></div>', unsafe_allow_html=True)

st.write("Selecciona un sector, ingresa los datos y calcula los resultados de forma automática.")

sector = st.selectbox("Elige el sector económico:", ["Tecnología / Software", "Manufactura", "Comercio / Retail"])
st.divider()

if sector == "Tecnología / Software":
    st.subheader("💻 Sector Tecnológico (Cálculo de Licencias / SaaS)")
    usuarios = st.number_input("Número de usuarios activos:", min_value=1, value=50, step=1)
    costo_por_usuario = st.number_input("Costo mensual por usuario ($):", min_value=0.0, value=15.0, step=0.5)
    descuento = st.number_input("Descuento aplicado (%):", min_value=0, max_value=100, value=5, step=1)
    if st.button("Calcular Total"):
        subtotal = usuarios * costo_por_usuario
        total = subtotal * (1 - descuento / 100)
        st.success(f"Costo Total Mensual: ${total:.2f}")
elif sector == "Manufactura":
    st.subheader("⚙️ Sector Manufactura (Cálculo de Producción)")
    unidades = st.number_input("Unidades a producir:", min_value=1, value=1000, step=10)
    costo_material = st.number_input("Costo de material por unidad ($):", min_value=0.0, value=5.5, step=0.1)
    costo_operativo_fijo = st.number_input("Costos operativos fijos ($):", min_value=0.0, value=2000.0, step=50.0)
    if st.button("Calcular Costo de Producción"):
        total = (unidades * costo_material) + costo_operativo_fijo
        costo_unitario_real = total / unidades
        st.success(f"Costo de Producción Total: ${total:.2f}")
        st.info(f"Costo por unidad fabricada: ${costo_unitario_real:.2f}")
elif sector == "Comercio / Retail":
    st.subheader("🛍️ Sector Comercio (Cálculo de Margen y Venta)")
    costo_producto = st.number_input("Costo de adquisición del producto ($):", min_value=0.0, value=50.0, step=1.0)
    margen_ganancia = st.number_input("Margen de ganancia deseado (%):", min_value=1, max_value=500, value=30, step=5)
    impuesto = st.number_input("Impuesto local / IVA (%):", min_value=0.0, value=16.0, step=0.5)
    if st.button("Calcular Precio de Venta"):
        precio_base = costo_producto * (1 + margen_ganancia / 100)
        precio_final = precio_base * (1 + impuesto / 100)
        ganancia_neta = precio_final - costo_producto
        st.success(f"Precio de Venta al Público: ${precio_final:.2f}")
        st.info(f"Ganancia neta por producto: ${ganancia_neta:.2f}") 
