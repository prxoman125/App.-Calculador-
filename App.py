import streamlit as st

# Configuración de página e inyección de CSS avanzado
st.set_page_config(page_title="Calculadora por Sectores", layout="centered")

st.markdown("""
    <style>
    /* Ocultar el menú superior (Share, GitHub, etc.) y el pie de página */
    #MainMenu, header, footer {
        visibility: hidden !important;
    }
    
    /* === BANNER DEL TÍTULO PROFESIONAL CON DEGRADADO Y BORDE NEÓN OSCURO === */
    .titulo-container {
        background: linear-gradient(135deg, #0A192F, #120D24, #1A0B2E, #0A192F);
        background-size: 300% 300%;
        animation: neonGradientAnimation 8s ease infinite;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 28px;
        border: 3px solid #1A365D;
    }
    
    .titulo-texto {
        color: #FFFFFF !important;
        font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        font-size: 30px;
        letter-spacing: -0.5px;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    @keyframes neonGradientAnimation {
        0% {
            background-position: 0% 50%;
            border-color: #1A365D;
            box-shadow: 0 0 15px rgba(26, 54, 93, 0.6);
        }
        50% {
            background-position: 100% 50%;
            border-color: #4C1D95;
            box-shadow: 0 0 15px rgba(76, 29, 149, 0.6);
        }
        100% {
            background-position: 0% 50%;
            border-color: #1A365D;
            box-shadow: 0 0 15px rgba(26, 54, 93, 0.6);
        }
    }
    
    /* === ESTILO PARA EL RECUADRO FÍSICO CON DEGRADADO GRIS OSCURO A NEGRO === */
    div[data-testid="stNumberInput"] > div:first-of-type, 
    div[data-testid="stSelectbox"] > div:first-of-type > div {
        border: 2px solid #1A365D !important;
        border-radius: 8px !important;
        transition: all 0.25s ease-in-out !important;
        background: linear-gradient(135deg, #22252A, #0F1115) !important;
    }

    /* Quita los fondos grises y bordes que Streamlit superpone de forma interna */
    div[data-testid="stNumberInput"] div, 
    div[data-testid="stSelectbox"] div {
        border: none !important;
        background-color: transparent !important;
    }

    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        color: #FFFFFF !important;
    }

    /* === EFECTO DE INTERACCIÓN Y BRILLO NEÓN (SÓLO RECUADRO) === */
    div[data-testid="stNumberInput"] > div:first-of-type:hover,
    div[data-testid="stNumberInput"] > div:first-of-type:focus-within,
    div[data-testid="stSelectbox"] > div:first-of-type > div:hover,
    div[data-testid="stSelectbox"] > div:first-of-type > div:focus-within {
        border-color: #2B6CB0 !important;
        box-shadow: 0 0 12px rgba(43, 108, 176, 0.55) !important;
    }
    
    /* === NUEVO DISEÑO FUSIONADO PARA LOS BOTONES MÁS Y MENOS === */
    /* Contenedor vertical de botones: se elimina el fondo gris interno y el gap a 0px */
    div[data-testid="stNumberInputStepUpAndDown"] {
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: stretch !important;
        padding: 0 !important;
        gap: 0px !important; /* Fusiona por completo ambas celdas eliminando espacios vacíos */
        overflow: hidden !important;
        border-radius: 0px 6px 6px 0px !important;
        /* Degradado de dos tonos de azul que cubre verticalmente todo el bloque de botones */
        background: linear-gradient(to bottom, #2B6CB0, #1A365D) !important;
    }

    /* Estilo estructural base para los botones individuales */
    button[data-testid="stNumberInputStepUp"], 
    button[data-testid="stNumberInputStepDown"] {
        height: 50% !important; /* Cada botón toma exactamente la mitad del alto */
        flex-grow: 1 !important;
        margin: 0 !important;
        border-radius: 0px !important; /* Quitamos bordes internos individuales */
        border: none !important;
        color: white !important;
        /* Hacemos el fondo del botón transparente para que se transparente el degradado de abajo */
        background-color: transparent !important; 
        transition: background-color 0.2s ease-in-out !important;
    }

    /* Efectos hover sutiles para oscurecer ligeramente la zona donde está el cursor */
    button[data-testid="stNumberInputStepUp"]:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    button[data-testid="stNumberInputStepDown"]:hover {
        background-color: rgba(0, 0, 0, 0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Renderizado del título profesional usando el contenedor CSS personalizado
st.markdown('<div class="titulo-container"><p class="titulo-texto">Calculadora Interactiva por Sectores</p></div>', unsafe_allow_html=True)

st.write("Selecciona un sector, ingresa los datos y calcula los resultados de forma automática.")

# Menú de selección de sector
sector = st.selectbox(
    "Elige el sector económico:",
    ["Tecnología / Software", "Manufactura", "Comercio / Retail"]
)

st.divider()

# Lógica condicional según el sector seleccionado
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
    st.subheader("⚙️ Sector Manufactura (Cálculo de Production)")
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
        ganancia_neta = precio_base - costo_producto
        st.success(f"Precio de Venta al Público: ${precio_final:.2f}")
        st.info(f"Ganancia neta por producto: ${ganancia_neta:.2f}")
 
