import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone

st.set_page_config(page_title="Calculadora por Sectores / Sector Calculator", layout="centered")

if "idioma" not in st.session_state:
    st.session_state.idioma = "Español"
if "historial" not in st.session_state:
    st.session_state.historial = []

# Zona horaria México Centro (León, GTO) UTC-6
ZONA_MEXICO = timezone(timedelta(hours=-6))

def guardar_en_tabla(sector, detalle, resultado):
    if len(st.session_state.historial) >= 15:
        st.session_state.historial.pop(0)
    hora_mexico = datetime.now(ZONA_MEXICO).strftime("%H:%M:%S")
    st.session_state.historial.append({
        "Hora": hora_mexico,
        "Sector": sector,
        "Detalle": detalle,
        "Resultado": resultado
    })

st.markdown("""
    <style>
    #MainMenu, header, footer { visibility: hidden !important; }
    p, label, span, div[data-testid="stMarkdownContainer"] p, 
    .st-emotion-cache-1gulkj5 p, [data-testid="stWidgetLabel"] p {
        color: #93C5FD !important;
    }
    h3, [data-testid="stSubheader"] {
        color: #BFDBFE !important;
        font-weight: 700 !important;
    }
    .titulo-container {
  background: linear-gradient(135deg, #00f0ff 0%, #8b00ff 50%, #0033cc 100%);
  background-size: 300% 300%;
  animation: fondoAzulClaroOscuro 6s ease-in-out infinite;
  padding: 24px;
  border-radius: 12px;
  text-align: center;
  margin-bottom: 28px;
  border: 3px solid #00f0ff;
}

@keyframes fondoAzulClaroOscuro {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

    }
    .titulo-texto {
        color: #FFFFFF !important;
        background: none !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 800;
        font-size: 30px;
        letter-spacing: -0.5px;
        margin: 0 !important;
        padding: 0 !important;
        display: inline-block;
    }
    /* Fondo oscuro -> claro y margen neón sincronizado */
    @keyframes fondoAzulClaroOscuro {
        0% {
            background-position: 0% 50%;
            border-color: #020617;
            box-shadow: 0 0 10px rgba(2, 6, 23, 0.8), 0 0 20px rgba(30, 58, 138, 0.4);
        }
        50% {
            background-position: 100% 50%;
            border-color: #60a5fa;
            box-shadow: 0 0 12px rgba(59, 130, 246, 0.9), 0 0 25px rgba(96, 165, 250, 0.6);
        }
        100% {
            background-position: 0% 50%;
            border-color: #020617;
            box-shadow: 0 0 10px rgba(2, 6, 23, 0.8), 0 0 20px rgba(30, 58, 138, 0.4);
        }
    }
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
    }
    div[data-testid="stNotificationV2"]:has(svg[title="Info"]),
    div[role="alert"]:has(svg[title="Info"]),
    .stAlert:has(svg[title="Info"]) {
        background: linear-gradient(135deg, #3B82F6, #1E3A8A) !important;
        border: 2px solid #3B82F6 !important;
        color: #FFFFFF !important;
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
        color: #93C5FD !important;
        text-align: center !important;
        padding-left: 80px !important;
        padding-right: 90px !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] span, 
    div[data-baseweb="select"] div,
    .stSelectbox div[data-baseweb="select"] {
        color: #93C5FD !important;
    }
    div[data-testid="stNumberInput"] > div:first-of-type:hover,
    div[data-testid="stNumberInput"] > div:first-of-type:focus-within,
    div[data-testid="stSelectbox"] > div:first-of-type > div:hover,
    div[data-testid="stSelectbox"] > div:first-of-type > div:focus-within {
        border-color: #2B6CB0 !important;
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
        transform: translateY(-50%) scale(0.92) !important;
    }
    </style>
""", unsafe_allow_html=True)

TEXTOS = {
    "Español": {
        "titulo": "Calculadora Interactiva por Sectores",
        "descripcion": "Selecciona un sector, ingresa los datos y calcula los resultados de forma automática.",
        "lbl_sector": "Elige el sector económico:",
        "sectores": ["Tecnología / Software","Manufactura","Comercio / Retail","Salud / Clínica","Construcción / Obras"],
        "btn_cambiar_idioma": "Switch to English",
        "tech_sub": "💻 Sector Tecnológico (Cálculo de Licencias / SaaS)", "tech_u": "Número de usuarios activos:", "tech_c": "Costo mensual por usuario ($):", "tech_d": "Descuento aplicado (%):", "tech_btn": "Calcular Total", "tech_res": "Costo Total Mensual: ${:.2f}",
        "man_sub": "⚙️ Sector Manufactura (Cálculo de Producción)", "man_u": "Unidades a producir:", "man_m": "Costo de material por unidad ($):", "man_f": "Costos operativos fijos ($):", "man_btn": "Calcular Costo de Producción", "man_res1": "Costo de Producción Total: ${:.2f}", "man_res2": "Costo por unidad fabricada: ${:.2f}",
        "com_sub": "🛍️ Sector Comercio (Cálculo de Margen y Venta)", "com_c": "Costo de adquisición del producto ($):", "com_m": "Margen de ganancia deseado (%):", "com_i": "Impuesto local / IVA (%):", "com_btn": "Calcular Precio de Venta", "com_res1": "Precio de Venta al Público: ${:.2f}", "com_res2": "Ganancia neta por producto: ${:.2f}",
        "sal_sub": "🏥 Sector Salud (Cálculo de Consultas y Procedimientos)", "sal_c": "Número de consultas estimadas:", "sal_p": "Precio base por consulta ($):", "sal_o": "Costos operativos por consulta ($):", "sal_btn": "Calcular Rentabilidad Clínica", "sal_res1": "Ingresos Brutos Estimados: ${:.2f}", "sal_res2": "Ganancia Neta Estimada: ${:.2f}",
        "con_sub": "🏗️ Sector Construcción (Cálculo de Presupuesto por m²)", "con_m": "Metros cuadrados (m²):", "con_c": "Costo de materiales por m² ($):", "con_o": "Costo de mano de obra por m² ($):", "con_btn": "Calcular Presupuesto Obra", "con_res1": "Presupuesto Total Estimado: ${:.2f}", "con_res2": "Costo Total por m²: ${:.2f}",
        "hist_titulo": "📊 Tabla de Registros (1 mínimo / 15 máximo)", "hist_vacio": "Aún no hay registros.", "btn_borrar": "🗑️ Borrar todas las tablas"
    },
    "English": {
        "titulo": "Interactive Sector Calculator",
        "descripcion": "Select a sector, enter data, and calculate results automatically.",
        "lbl_sector": "Choose the economic sector:",
        "sectores": ["Technology / Software","Manufacturing","Retail / Commerce","Healthcare / Clinic","Construction / Building"],
        "btn_cambiar_idioma": "Cambiar a Español",
        "tech_sub": "💻 Technology Sector (SaaS / Licensing Calculation)", "tech_u": "Number of active users:", "tech_c": "Monthly cost per user ($):", "tech_d": "Applied discount (%):", "tech_btn": "Calculate Total", "tech_res": "Total Monthly Cost: ${:.2f}",
        "man_sub": "⚙️ Manufacturing Sector (Production Calculation)", "man_u": "Units to produce:", "man_m": "Material cost per unit ($):", "man_f": "Fixed operational costs ($):", "man_btn": "Calculate Production Cost", "man_res1": "Total Production Cost: ${:.2f}", "man_res2": "Cost per manufactured unit: ${:.2f}",
        "com_sub": "🛍️ Retail Sector (Margin & Sale Calculation)", "com_c": "Product acquisition cost ($):", "com_m": "Desired profit margin (%):", "com_i": "Local tax / VAT (%):", "com_btn": "Calculate Selling Price", "com_res1": "Public Retail Price: ${:.2f}", "com_res2": "Net profit per product: ${:.2f}",
        "sal_sub": "🏥 Healthcare Sector (Consultation & Procedure Calculation)", "sal_c": "Estimated number of consultations:", "sal_p": "Base price per consultation ($):", "sal_o": "Operating cost per consultation ($):", "sal_btn": "Calculate Clinic Profitability", "sal_res1": "Estimated Gross Revenue: ${:.2f}", "sal_res2": "Estimated Net Profit: ${:.2f}",
        "con_sub": "🏗️ Construction Sector (Budget per m² Calculation)", "con_m": "Square meters (m²):", "con_c": "Material cost per m² ($):", "con_o": "Labor cost per m² ($):", "con_btn": "Calculate Construction Budget", "con_res1": "Total Estimated Budget: ${:.2f}", "con_res2": "Total Cost per m²: ${:.2f}",
        "hist_titulo": "📊 Records Table (1 min / 15 max)", "hist_vacio": "No records yet.", "btn_borrar": "🗑️ Clear all tables"
    }
}

txt = TEXTOS[st.session_state.idioma]
st.markdown(f'<div class="titulo-container"><span class="titulo-texto">{txt["titulo"]}</span></div>', unsafe_allow_html=True)
st.write(txt["descripcion"])
sector = st.selectbox(txt["lbl_sector"], txt["sectores"])
if st.button(txt["btn_cambiar_idioma"]):
    st.session_state.idioma = "English" if st.session_state.idioma == "Español" else "Español"
    st.rerun()
st.divider()

if sector in ["Tecnología / Software", "Technology / Software"]:
    st.subheader(txt["tech_sub"])
    usuarios = st.number_input(txt["tech_u"], min_value=1, value=50, step=1)
    costo_por_usuario = st.number_input(txt["tech_c"], min_value=0.0, value=15.0, step=0.5)
    descuento = st.number_input(txt["tech_d"], min_value=0, max_value=100, value=5, step=1)
    if st.button(txt["tech_btn"]):
        total = usuarios * costo_por_usuario * (1 - descuento / 100)
        st.success(txt["tech_res"].format(total))
        guardar_en_tabla(sector, f"{usuarios}u x ${costo_por_usuario} -{descuento}%", f"${total:.2f}")

elif sector in ["Manufactura", "Manufacturing"]:
    st.subheader(txt["man_sub"])
    unidades = st.number_input(txt["man_u"], min_value=1, value=1000, step=10)
    costo_material = st.number_input(txt["man_m"], min_value=0.0, value=5.5, step=0.1)
    costo_operativo_fijo = st.number_input(txt["man_f"], min_value=0.0, value=2000.0, step=50.0)
    if st.button(txt["man_btn"]):
        total = (unidades * costo_material) + costo_operativo_fijo
        st.success(txt["man_res1"].format(total))
        st.info(txt["man_res2"].format(total / unidades))
        guardar_en_tabla(sector, f"{unidades}u | mat ${costo_material} + fijo ${costo_operativo_fijo}", f"${total:.2f}")

elif sector in ["Comercio / Retail", "Retail / Commerce"]:
    st.subheader(txt["com_sub"])
    costo_producto = st.number_input(txt["com_c"], min_value=0.0, value=50.0, step=1.0)
    margen_ganancia = st.number_input(txt["com_m"], min_value=1, max_value=500, value=30, step=5)
    impuesto = st.number_input(txt["com_i"], min_value=0.0, value=16.0, step=0.5)
    if st.button(txt["com_btn"]):
        precio_base = costo_producto * (1 + margen_ganancia / 100)
        precio_final = precio_base * (1 + impuesto / 100)
        st.success(txt["com_res1"].format(precio_final))
        st.info(txt["com_res2"].format(precio_base - costo_producto))
        guardar_en_tabla(sector, f"Costo ${costo_producto} + {margen_ganancia}% + IVA {impuesto}%", f"${precio_final:.2f}")

elif sector in ["Salud / Clínica", "Healthcare / Clinic"]:
    st.subheader(txt["sal_sub"])
    consultas = st.number_input(txt["sal_c"], min_value=1, value=120, step=5)
    precio_consulta = st.number_input(txt["sal_p"], min_value=0.0, value=60.0, step=5.0)
    costo_operativo = st.number_input(txt["sal_o"], min_value=0.0, value=20.0, step=2.0)
    if st.button(txt["sal_btn"]):
        ingresos = consultas * precio_consulta
        ganancia = consultas * (precio_consulta - costo_operativo)
        st.success(txt["sal_res1"].format(ingresos))
        st.info(txt["sal_res2"].format(ganancia))
        guardar_en_tabla(sector, f"{consultas} cons x ${precio_consulta} - ${costo_operativo} costo", f"${ganancia:.2f}")

elif sector in ["Construcción / Obras", "Construction / Building"]:
    st.subheader(txt["con_sub"])
    metros = st.number_input(txt["con_m"], min_value=1.0, value=150.0, step=10.0)
    costo_material_m2 = st.number_input(txt["con_c"], min_value=0.0, value=120.0, step=5.0)
    costo_obra_m2 = st.number_input(txt["con_o"], min_value=0.0, value=80.0, step=5.0)
    if st.button(txt["con_btn"]):
        costo_m2_total = costo_material_m2 + costo_obra_m2
        total = metros * costo_m2_total
        st.success(txt["con_res1"].format(total))
        st.info(txt["con_res2"].format(costo_m2_total))
        guardar_en_tabla(sector, f"{metros} m² x (${costo_material_m2}+${costo_obra_m2})", f"${total:.2f}")

st.divider()
st.subheader(txt["hist_titulo"])

if st.session_state.historial:
    df = pd.DataFrame(st.session_state.historial)
    st.dataframe(df, use_container_width=True, hide_index=True)
    if st.button(txt["btn_borrar"]):
        st.session_state.historial = []
        st.rerun()
else:
    st.info(txt["hist_vacio"])
