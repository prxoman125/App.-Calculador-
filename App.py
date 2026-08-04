import streamlit as st

# Configuración de página e inyección de CSS avanzado
st.set_page_config(page_title="Calculadora por Sectores", layout="centered")

st.markdown("""
    <style>
    /* Ocultar el menú superior (Share, GitHub, etc.) y el pie de página */
    #MainMenu, header, footer {
        visibility: hidden !important;
    }
    
    /* === BANNER DEL TÍTULO CON DEGRADADO INTERNO MONOCROMÁTICO Y SINCRONIZACIÓN TOTAL === */
    .titulo-container {
        /* Degradado que viaja de tonos base a sus versiones intensas de la misma gama */
        background: linear-gradient(135deg, #0A192F, #1E3A8A, #1E0B36, #5B21B6, #1A0B2E, #0A192F);
        background-size: 400% 400%;
        
        /* Una única animación controla la velocidad del fondo, borde y sombra simultáneamente */
        animation: neonSincronizadoAnimation 14s ease infinite;
        
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 28px;
        border: 3px solid #0A192F;
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
    
    /* Transición exacta y a la misma velocidad para el fondo, el color del margen y su brillo neón */
    @keyframes neonSincronizadoAnimation {
        0%, 100% {
            background-position: 0% 50%;
            border-color: #1E3A8A; /* Margen: Azul oscuro a azul intenso */
            box-shadow: 0 0 22px rgba(30, 58, 138, 0.8);
        }
        50% {
            background-position: 50% 50%;
            border-color: #5B21B6; /* Margen: Morado oscuro a morado intenso */
            box-shadow: 0 0 22px rgba(91, 33, 182, 0.8);
        }
    }
    
    /* === CORRECCIÓN DEFINITIVA DE LAS BARRAS DE RESULTADOS (DEGRADADOS REALES) === */
    /* Caja Verde (st.success) -> De verde claro/vivo a verde oscuro profundo */
    .stAlert:has(div[data-testid="stNotificationContentSuccess"]),
    div[role="alert"]:has(svg[title="Success"]),
    div[data-testid="stNotificationV2"]:has(svg[title="Success"]) {
        background: linear-gradient(135deg, #10B981, #064E3B) !important;
        color: #FFFFFF !important;
        border: 1px solid #10B981 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 10px rgba(6, 78, 59, 0.3) !important;
    }
    
    /* Caja Azul (st.info) -> De azul claro/vivo a azul oscuro profundo */
    .stAlert:has(div[data-testid="stNotificationContentInfo"]),
    div[role="alert"]:has(svg[title="Info"]),
    div[data-testid="stNotificationV2"]:has(svg[title="Info"]) {
        background: linear-gradient(135deg, #3B82F6, #1E3A8A) !important;
        color: #FFFFFF !important;
        border: 1px solid #3B82F6 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 10px rgba(30, 58, 138, 0.3) !important;
    }
    
    /* Forzar a que todo el contenido de texto dentro de los bloques de resultado sea blanco */
    .stAlert p, .stAlert div, div[role="alert"] p, div[role="alert"] div {
        color: #FFFFFF !important;
    }

    /* === ESTILO PARA EL RECUADRO FÍSICO CON DEGRADADO GRIS OSCURO A NEGRO === */
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

    /* === ALINEACIÓN AL CENTRO PARA LOS NÚMEROS === */
    .stNumberInput input {
        color: #FFFFFF !important;
        text-align: center !important;
        padding-left: 80px !important;
        padding-right: 90px !important;
    }
    
    .stSelectbox div[data-baseweb="select"] {
        color: #FFFFFF !important;
    }

    /* === EFECTO DE INTERACCIÓN Y BRILLO NEÓN EN EL RECUADRO PRINCIPAL === */
    div[data-testid="stNumberInput"] > div:first-of-type:hover,
    div[data-testid="stNumberInput"] > div:first-of-type:focus-within,
    div[data-testid="stSelectbox"] > div:first-of-type > div:hover,
    div[data-testid="stSelectbox"] > div:first-of-type > div:focus-within {
        border-color: #2B6CB0 !important;
        box-shadow: 0 0 12px rgba(43, 108, 176, 0.55) !important;
    }
    
    /* === CONTROL ABSOLUTO HORIZONTAL COMPLETO === */
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

    button[data-testid="stNumberInputStepDown"] {
        left: 6px !important;
    }

    button[data-testid="stNumberInputStepUp"] {
        right: 6px !important;
    }

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
        ganancia_neta = precio_base - costo_producto
        st.success(f"Precio de Venta al Público: ${precio_final:.2f}")
        st.info(f"Ganancia neta por producto: ${ganancia_neta:.2f}")
 
