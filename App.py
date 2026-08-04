import streamlit as st

# Configuración de página e inyección de CSS avanzado
st.set_page_config(page_title="Calculadora por Sectores", layout="centered")

st.markdown("""
    <style>
    /* Ocultar el menú superior (Share, GitHub, etc.) y el pie de página */
    #MainMenu, header, footer {
        visibility: hidden !important;
    }
    
    /* === ESTILO DE LAS CAJAS DE INGRESO DE DATOS (SÓLO EL RECUADRO) === */
    /* Apunta de forma precisa al contenedor del input y del selectbox sin tocar sus etiquetas superiores */
    div[data-testid="stNumberInput"] > div[data-baseweb="base-input"], 
    div[data-testid="stSelectbox"] > div[data-baseweb="select"] {
        border: 2px solid #1A365D !important; /* Borde azul oscuro base (combina con botón menos) */
        border-radius: 8px !important;
        transition: all 0.3s ease-in-out !important;
        background-color: transparent !important;
    }

    /* Eliminar bordes nativos internos para evitar duplicaciones visuales */
    div[data-testid="stNumberInput"] > div[data-baseweb="base-input"] > div {
        border: none !important;
    }

    /* EFECTO HOVER Y ENFOQUE SÓLO EN EL RECUADRO: Brillo neón sutil al interactuar */
    div[data-testid="stNumberInput"] > div[data-baseweb="base-input"]:focus-within, 
    div[data-testid="stSelectbox"] > div[data-baseweb="select"]:focus-within,
    div[data-testid="stNumberInput"] > div[data-baseweb="base-input"]:hover,
    div[data-testid="stSelectbox"] > div[data-baseweb="select"]:hover {
        border-color: #2B6CB0 !important; /* Cambia al azul más claro (combina con botón más) */
        /* Sutil sombra neón difuminada sin molestar a la vista */
        box-shadow: 0 0 10px rgba(43, 108, 176, 0.4) !important; 
    }
    
    /* === AJUSTE DE LOS BOTONES MÁS Y MENOS === */
    /* Configurar el contenedor para usar todo el alto sin bordes grises vacíos */
    div[data-testid="stNumberInputStepUpAndDown"] {
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        padding: 0 !important;
        gap: 2px !important;
    }

    /* Estilos generales para ambos botones */
    button[data-testid="stNumberInputStepUp"], 
    button[data-testid="stNumberInputStepDown"] {
        height: 100% !important;
        flex-grow: 1 !important;
        margin: 0 !important;
        border-radius: 0px 6px 6px 0px !important; /* Ajustado al nuevo radio del recuadro */
        border: none !important;
        color: white !important;
    }

    /* BOTÓN MENOS (-): Azul Oscuro Clásico */
    button[data-testid="stNumberInputStepDown"] {
        background-color: #1A365D !important;
    }
    button[data-testid="stNumberInputStepDown"]:hover {
        background-color: #10243F !important;
    }

    /* BOTÓN MÁS (+): Azul Más Claro / Eléctrico */
    button[data-testid="stNumberInputStepUp"] {
        background-color: #2B6CB0 !important;
    }
    button[data-testid="stNumberInputStepUp"]:hover {
        background-color: #1D4ED8 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Calculadora Interactiva por Sectores")
st.write("Selecciona un sector, ingresa los datos y calcula los resultados de forma automática.")

# Menú de selección de sector (también hereda el diseño del borde limpio)
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
