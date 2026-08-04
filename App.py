import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone

st.set_page_config(page_title="Calculadora por Sectores / Sector Calculator", layout="centered")

if "idioma" not in st.session_state:
    st.session_state.idioma = "Español"
if "historial" not in st.session_state:
    st.session_state.historial = []

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    #MainMenu, header, footer { visibility: hidden !important; }
    
    .stApp {
        background: radial-gradient(1200px 600px at 20% -10%, #2A2A2A 0%, transparent 60%),
                    radial-gradient(1000px 500px at 90% 110%, #4A4A4A 0%, transparent 60%),
                    linear-gradient(135deg, #000000 0%, #141414 35%, #2E2E2E 100%) !important;
    }
    [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2.5rem !important;
    }
    p, label, span, div[data-testid="stMarkdownContainer"] p, 
    .st-emotion-cache-1gulkj5 p, [data-testid="stWidgetLabel"] p {
        color: #E5E7EB !important;
        letter-spacing: 0.2px !important;
    }
    [data-testid="stWidgetLabel"] p { 
        font-weight: 600 !important; 
        font-size: 13px !important; 
        text-transform: uppercase !important; 
        letter-spacing: 0.8px !important; 
        color: #9CA3AF !important; 
    }
    
    h3, [data-testid="stSubheader"] {
        background: linear-gradient(135deg, rgba(26,26,26,0.9) 0%, rgba(45,45,45,0.85) 100%) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-left: 3px solid #FFFFFF !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        letter-spacing: -0.2px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.05) inset, 0 1px 0 rgba(255,255,255,0.1) inset !important;
    }
    
    .titulo-container {
      background: linear-gradient(135deg, rgba(0,0,0,0.9) 0%, rgba(30,30,30,0.9) 50%, rgba(70,70,70,0.8) 100%);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      padding: 28px 24px;
      border-radius: 16px;
      text-align: center;
      border: 1px solid rgba(255,255,255,0.12) !important;
      box-shadow: 0 8px 32px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.06) inset, 0 1px 0 rgba(255,255,255,0.15) inset !important;
      position: relative;
      overflow: hidden;
    }
    .titulo-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    }
    .titulo-texto {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 27px !important;
        letter-spacing: -0.6px !important;
        line-height: 1.2 !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5) !important;
    }
    
    div[data-testid="stDataFrame"] {
        background: rgba(20,20,20,0.7) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4) !important;
    }
    
    div[data-testid="stNotificationV2"], div[role="alert"], div.stAlert {
        backdrop-filter: blur(16px) !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }
    div[data-testid="stNotificationV2"]:has(svg[title="Success"]),
    div[role="alert"]:has(svg[title="Success"]) {
        background: linear-gradient(135deg, rgba(38,38,38,0.95) 0%, rgba(10,10,10,0.98) 100%) !important;
        border: 1px solid rgba(255,255,255,0.9) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.6), 0 0 20px rgba(255,255,255,0.15), 0 0 0 1px rgba(255,255,255,0.1) inset !important;
    }
    div[data-testid="stNotificationV2"]:has(svg[title="Info"]),
    div[role="alert"]:has(svg[title="Info"]) {
        background: linear-gradient(135deg, rgba(60,60,60,0.9) 0%, rgba(30,30,30,0.95) 100%) !important;
        border: 1px solid rgba(229,231,235,0.5) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5), 0 0 16px rgba(255,255,255,0.08) !important;
    }
    
    /* Inputs premium */
    div[data-testid="stNumberInput"] > div:first-of-type, 
    div[data-testid="stSelectbox"] > div:first-of-type > div {
        background: linear-gradient(135deg, rgba(28,28,28,0.9) 0%, rgba(15,15,15,0.95) 100%) !important;
        backdrop-filter: blur(8px) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
        transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3), 0 0 0 1px rgba(255,255,255,0.03) inset !important;
    }
    div[data-testid="stNumberInput"] > div:first-of-type:hover,
    div[data-testid="stSelectbox"] > div:first-of-type > div:hover {
        border-color: rgba(255,255,255,0.35) !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.4), 0 0 12px rgba(255,255,255,0.12) !important;
        transform: translateY(-1px);
    }
    div[data-testid="stNumberInput"] > div:first-of-type:focus-within,
    div[data-testid="stSelectbox"] > div:first-of-type > div:focus-within {
        border-color: #FFFFFF !important;
        box-shadow: 0 0 0 3px rgba(255,255,255,0.12), 0 8px 24px rgba(0,0,0,0.5), 0 0 20px rgba(255,255,255,0.15) !important;
        transform: translateY(-1px);
    }
    .stNumberInput input {
        color: #FFFFFF !important;
        text-align: center !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
    }
    div[data-baseweb="select"] span { color: #FFFFFF !important; font-weight: 500 !important; }
    
    /* Botones alta gama */
    button[kind="secondary"], .stButton > button {
        background: linear-gradient(135deg, #2A2A2A 0%, #0A0A0A 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        font-size: 12px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.05) inset !important;
        transition: all 0.3s ease !important;
    }
    button[kind="secondary"]:hover, .stButton > button:hover {
        background: linear-gradient(135deg, #FFFFFF 0%, #D1D5DB 100%) !important;
        color: #000000 !important;
        border-color: #FFFFFF !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5), 0 0 20px rgba(255,255,255,0.2) !important;
        transform: translateY(-2px) !important;
    }
    hr { border-color: rgba(255,255,255,0.08) !important; margin: 28px 0 !important; }
    </style>
""", unsafe_allow_html=True)

TEXTOS = {
    "Español": {
        "titulo": "Calculadora Interactiva por Sectores",
        "descripcion": "Selecciona un sector, ingresa los datos y calcula los resultados de forma automática.",
        "lbl_sector": "Elige el sector económico:",
        "sectores": ["Tecnología / Software","Manufactura","Comercio / Retail","Salud / Clínica","Construcción / Obras","Finanzas / Inversión","Educación / Formación"],
        "btn_cambiar_idioma": "Switch to English",
        "tech_sub": "💻 Sector Tecnológico (Cálculo de Licencias / SaaS)", "tech_u": "Número de usuarios activos:", "tech_c": "Costo mensual por usuario ($):", "tech_d": "Descuento aplicado (%):", "tech_btn": "Calcular Total", "tech_res": "Costo Total Mensual: ${:.2f}",
        "man_sub": "⚙️ Sector Manufactura (Cálculo de Producción)", "man_u": "Unidades a producir:", "man_m": "Costo de material por unidad ($):", "man_f": "Costos operativos fijos ($):", "man_btn": "Calcular Costo de Producción", "man_res1": "Costo de Producción Total: ${:.2f}", "man_res2": "Costo por unidad fabricada: ${:.2f}",
        "com_sub": "🛍️ Sector Comercio (Cálculo de Margen y Venta)", "com_c": "Costo de adquisición del producto ($):", "com_m": "Margen de ganancia deseado (%):", "com_i": "Impuesto local / IVA (%):", "com_btn": "Calcular Precio de Venta", "com_res1": "Precio de Venta al Público: ${:.2f}", "com_res2": "Ganancia neta por producto: ${:.2f}",
        "sal_sub": "🏥 Sector Salud (Cálculo de Consultas y Procedimientos)", "sal_c": "Número de consultas estimadas:", "sal_p": "Precio base por consulta ($):", "sal_o": "Costos operativos por consulta ($):", "sal_btn": "Calcular Rentabilidad Clínica", "sal_res1": "Ingresos Brutos Estimados: ${:.2f}", "sal_res2": "Ganancia Neta Estimada: ${:.2f}",
        "con_sub": "🏗️ Sector Construcción (Cálculo de Presupuesto por m²)", "con_m": "Metros cuadrados (m²):", "con_c": "Costo de materiales por m² ($):", "con_o": "Costo de mano de obra por m² ($):", "con_btn": "Calcular Presupuesto Obra", "con_res1": "Presupuesto Total Estimado: ${:.2f}", "con_res2": "Costo Total por m²: ${:.2f}",
        "fin_sub": "💹 Sector Finanzas (Cálculo de Interés Compuesto / ROI)", "fin_cap": "Capital inicial ($):", "fin_tasa": "Tasa anual (%):", "fin_anos": "Años de inversión:", "fin_btn": "Calcular Rendimiento", "fin_res1": "Monto Final Estimado: ${:.2f}", "fin_res2": "Ganancia Total: ${:.2f}",
        "edu_sub": "🎓 Sector Educación (Cálculo de Costo por Alumno)", "edu_al": "Número de alumnos:", "edu_cur": "Costo operativo del curso ($):", "edu_mat": "Costo material por alumno ($):", "edu_btn": "Calcular Costo Educativo", "edu_res1": "Costo Total del Programa: ${:.2f}", "edu_res2": "Costo por Alumno: ${:.2f}",
        "hist_titulo": "📊 Tabla de Registros (1 mínimo / 15 máximo)", "hist_vacio": "Aún no hay registros.", "btn_borrar": "🗑️ Borrar todas las tablas"
    },
    "English": {
        "titulo": "Interactive Sector Calculator",
        "descripcion": "Select a sector, enter data, and calculate results automatically.",
        "lbl_sector": "Choose the economic sector:",
        "sectores": ["Technology / Software","Manufacturing","Retail / Commerce","Healthcare / Clinic","Construction / Building","Finance / Investment","Education / Training"],
        "btn_cambiar_idioma": "Cambiar a Español",
        "tech_sub": "💻 Technology Sector (SaaS / Licensing Calculation)", "tech_u": "Number of active users:", "tech_c": "Monthly cost per user ($):", "tech_d": "Applied discount (%):", "tech_btn": "Calculate Total", "tech_res": "Total Monthly Cost: ${:.2f}",
        "man_sub": "⚙️ Manufacturing Sector (Production Calculation)", "man_u": "Units to produce:", "man_m": "Material cost per unit ($):", "man_f": "Fixed operational costs ($):", "man_btn": "Calculate Production Cost", "man_res1": "Total Production Cost: ${:.2f}", "man_res2": "Cost per manufactured unit: ${:.2f}",
        "com_sub": "🛍️ Retail Sector (Margin & Sale Calculation)", "com_c": "Product acquisition cost ($):", "com_m": "Desired profit margin (%):", "com_i": "Local tax / VAT (%):", "com_btn": "Calculate Selling Price", "com_res1": "Public Retail Price: ${:.2f}", "com_res2": "Net profit per product: ${:.2f}",
        "sal_sub": "🏥 Healthcare Sector (Consultation & Procedure Calculation)", "sal_c": "Estimated number of consultations:", "sal_p": "Base price per consultation ($):", "sal_o": "Operating cost per consultation ($):", "sal_btn": "Calculate Clinic Profitability", "sal_res1": "Estimated Gross Revenue: ${:.2f}", "sal_res2": "Estimated Net Profit: ${:.2f}",
        "con_sub": "🏗️ Construction Sector (Budget per m² Calculation)", "con_m": "Square meters (m²):", "con_c": "Material cost per m² ($):", "con_o": "Labor cost per m² ($):", "con_btn": "Calculate Construction Budget", "con_res1": "Total Estimated Budget: ${:.2f}", "con_res2": "Total Cost per m²: ${:.2f}",
        "fin_sub": "💹 Finance Sector (Compound Interest / ROI Calculation)", "fin_cap": "Initial capital ($):", "fin_tasa": "Annual rate (%):", "fin_anos": "Years of investment:", "fin_btn": "Calculate Yield", "fin_res1": "Estimated Final Amount: ${:.2f}", "fin_res2": "Total Profit: ${:.2f}",
        "edu_sub": "🎓 Education Sector (Cost per Student Calculation)", "edu_al": "Number of students:", "edu_cur": "Course operating cost ($):", "edu_mat": "Material cost per student ($):", "edu_btn": "Calculate Educational Cost", "edu_res1": "Total Program Cost: ${:.2f}", "edu_res2": "Cost per Student: ${:.2f}",
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
elif sector in ["Finanzas / Inversión", "Finance / Investment"]:
    st.subheader(txt["fin_sub"])
    capital = st.number_input(txt["fin_cap"], min_value=0.0, value=10000.0, step=500.0)
    tasa = st.number_input(txt["fin_tasa"], min_value=0.0, value=8.0, step=0.5)
    anos = st.number_input(txt["fin_anos"], min_value=1, value=5, step=1)
    if st.button(txt["fin_btn"]):
        monto_final = capital * ((1 + tasa/100) ** anos)
        ganancia = monto_final - capital
        st.success(txt["fin_res1"].format(monto_final))
        st.info(txt["fin_res2"].format(ganancia))
        guardar_en_tabla(sector, f"${capital} al {tasa}% x {anos}a", f"${monto_final:.2f}")
elif sector in ["Educación / Formación", "Education / Training"]:
    st.subheader(txt["edu_sub"])
    alumnos = st.number_input(txt["edu_al"], min_value=1, value=25, step=1)
    costo_curso = st.number_input(txt["edu_cur"], min_value=0.0, value=5000.0, step=100.0)
    costo_mat = st.number_input(txt["edu_mat"], min_value=0.0, value=50.0, step=5.0)
    if st.button(txt["edu_btn"]):
        total = costo_curso + (alumnos * costo_mat)
        por_alumno = total / alumnos
        st.success(txt["edu_res1"].format(total))
        st.info(txt["edu_res2"].format(por_alumno))
        guardar_en_tabla(sector, f"{alumnos} al x curso ${costo_curso}+${costo_mat}", f"${total:.2f}")

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
