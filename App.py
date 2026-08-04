import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import io

st.set_page_config(
    page_title="Calculadora por Sectores",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "idioma" not in st.session_state:
    st.session_state.idioma = "Español"
if "historial" not in st.session_state:
    st.session_state.historial = []

ZONA_MEXICO = timezone(timedelta(hours=-6))

def guardar_en_tabla(sector, detalle, resultado):
    if len(st.session_state.historial) >= 25:
        st.session_state.historial.pop(0)
    hora_mexico = datetime.now(ZONA_MEXICO).strftime("%H:%M:%S")
    st.session_state.historial.append({
        "Hora": hora_mexico,
        "Sector": sector,
        "Detalle": detalle,
        "Resultado": resultado
    })

def generar_excel(df):
    output = io.BytesIO()
    try:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Registros')
        output.seek(0)
        return output, "xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    except ModuleNotFoundError:
        output = io.BytesIO()
        output.write(df.to_csv(index=False).encode('utf-8'))
        output.seek(0)
        return output, "csv", "text/csv"

def generar_pdf(df):
    output = io.BytesIO()
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib import colors
        c = canvas.Canvas(output, pagesize=letter)
        width, height = letter
        c.setFillColor(colors.HexColor("#FFFFFF"))
        c.rect(0,0,width,height,fill=1)
        c.setFillColor(colors.HexColor("#111827"))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, height-50, "Tabla de Registros - Calculadora por Sectores")
        c.setFont("Helvetica", 9)
        y = height-80
        cols = list(df.columns)
        x_pos = [40, 110, 250, 410]
        for i, col in enumerate(cols):
            c.drawString(x_pos[i], y, str(col))
        y -= 16
        c.setStrokeColor(colors.HexColor("#E5E7EB"))
        c.line(40, y, width-40, y)
        y -= 12
        c.setFont("Helvetica", 8)
        for _, row in df.iterrows():
            if y < 50:
                c.showPage()
                y = height-50
            for i, col in enumerate(cols):
                c.drawString(x_pos[i], y, str(row[col])[:38])
            y -= 12
        c.save()
    except Exception:
        output.write(f"Tabla de Registros\n{df.to_string(index=False)}".encode('utf-8'))
    output.seek(0)
    return output

# --- ESTILO PROFESIONAL MONOCROMATICO LIMPIO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif!important; }
    #MainMenu, header, footer { visibility: hidden!important; }

    /* Fix borde rojo interior Streamlit */
    div[data-testid="stNumberInput"] > div:first-of-type {
        border: 1px solid #D1D5DB!important;
        box-shadow: none!important;
    }
    div[data-baseweb="base-input"], div[data-baseweb="input"] {
        border: none!important; box-shadow: none!important; background: transparent!important;
    }
    input, input:focus, input[aria-invalid="true"] {
        border: none!important; outline: none!important; box-shadow: none!important;
    }
    div[data-testid="stNumberInput"] * { --tw-ring-color: transparent!important; }

   .stApp {
        background: #F9FAFB!important;
    }
    [data-testid="stAppViewContainer"] { background: #F9FAFB!important; }
   .block-container {
        padding-top: 2.2rem!important;
        padding-bottom: 2rem!important;
        max-width: 760px!important;
    }

   .header-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 28px 24px;
        text-align: center;
        margin-bottom: 8px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03);
    }
   .header-title {
        color: #111827!important;
        font-weight: 700!important;
        font-size: 22px!important;
        letter-spacing: -0.3px!important;
        margin: 0!important;
    }
   .header-subtitle {
        color: #6B7280!important;
        font-size: 14px!important;
        font-weight: 400!important;
        margin-top: 6px!important;
    }

    p, label, span, div[data-testid="stMarkdownContainer"] p {
        color: #374151!important;
    }
    [data-testid="stWidgetLabel"] p {
        font-weight: 500!important;
        font-size: 12.5px!important;
        text-transform: uppercase!important;
        letter-spacing: 0.6px!important;
        color: #6B7280!important;
        margin-bottom: 6px!important;
    }

    h3, [data-testid="stSubheader"] {
        background: #FFFFFF!important;
        border: 1px solid #E5E7EB!important;
        border-left: 4px solid #111827!important;
        border-radius: 8px!important;
        padding: 12px 16px!important;
        color: #111827!important;
        font-weight: 600!important;
        font-size: 14.5px!important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04)!important;
    }

    div[data-testid="stDataFrame"] {
        background: #FFFFFF!important;
        border: 1px solid #E5E7EB!important;
        border-radius: 10px!important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04)!important;
    }

    div[data-testid="stNotificationV2"], div[role="alert"] {
        border-radius: 8px!important;
        border: 1px solid #E5E7EB!important;
        background: #FFFFFF!important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05)!important;
        color: #111827!important;
    }
    div[data-testid="stNotificationV2"] p, div[role="alert"] p {
        color: #111827!important;
        font-weight: 500!important;
        font-size: 14px!important;
    }

    div[data-testid="stNumberInput"] > div:first-of-type,
    div[data-testid="stSelectbox"] > div:first-of-type > div {
        background: #FFFFFF!important;
        border: 1px solid #D1D5DB!important;
        border-radius: 8px!important;
        height: 42px!important;
        transition: all 0.2s ease!important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03)!important;
    }
    div[data-testid="stNumberInput"] > div:first-of-type:hover,
    div[data-testid="stSelectbox"] > div:first-of-type > div:hover {
        border-color: #9CA3AF!important;
    }
    div[data-testid="stNumberInput"] > div:first-of-type:focus-within,
    div[data-testid="stSelectbox"] > div:first-of-type > div:focus-within {
        border-color: #111827!important;
        box-shadow: 0 0 0 3px rgba(17,24,39,0.08)!important;
    }
   .stNumberInput input {
        color: #111827!important;
        font-weight: 500!important;
        font-size: 14px!important;
    }
    div[data-baseweb="select"] span { color: #111827!important; }

   .stButton > button {
        background: #111827!important;
        color: #FFFFFF!important;
        border: 1px solid #111827!important;
        border-radius: 8px!important;
        padding: 10px 18px!important;
        font-weight: 600!important;
        font-size: 12.5px!important;
        letter-spacing: 0.4px!important;
        text-transform: uppercase!important;
        height: 40px!important;
        transition: all 0.2s ease!important;
    }
   .stButton > button:hover {
        background: #000000!important;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.15)!important;
    }
    hr { border-color: #E5E7EB!important; margin: 24px 0!important; }
    </style>
""", unsafe_allow_html=True)

TEXTOS = {
    "Español": {
        "titulo": "Calculadora Interactiva por Sectores",
        "descripcion": "Selecciona un sector, ingresa los datos y calcula los resultados de forma automatica.",
        "lbl_sector": "Elige el sector economico:",
        "sectores": ["Tecnologia / Software","Manufactura","Comercio / Retail","Salud / Clinica","Construccion / Obras","Finanzas / Inversion","Educacion / Formacion"],
        "btn_cambiar_idioma": "Switch to English",
        "tech_sub": "Sector Tecnologico (Calculo de Licencias / SaaS)", "tech_u": "Numero de usuarios activos:", "tech_c": "Costo mensual por usuario ($):", "tech_d": "Descuento aplicado (%):", "tech_btn": "Calcular Total", "tech_res": "Costo Total Mensual: ${:.2f}",
        "man_sub": "Sector Manufactura (Calculo de Produccion)", "man_u": "Unidades a producir:", "man_m": "Costo de material por unidad ($):", "man_f": "Costos operativos fijos ($):", "man_btn": "Calcular Costo de Produccion", "man_res1": "Costo de Produccion Total: ${:.2f}", "man_res2": "Costo por unidad fabricada: ${:.2f}",
        "com_sub": "Sector Comercio (Calculo de Margen y Venta)", "com_c": "Costo de adquisicion del producto ($):", "com_m": "Margen de ganancia deseado (%):", "com_i": "Impuesto local / IVA (%):", "com_btn": "Calcular Precio de Venta", "com_res1": "Precio de Venta al Publico: ${:.2f}", "com_res2": "Ganancia neta por producto: ${:.2f}",
        "sal_sub": "Sector Salud (Calculo de Consultas y Procedimientos)", "sal_c": "Numero de consultas estimadas:", "sal_p": "Precio base por consulta ($):", "sal_o": "Costos operativos por consulta ($):", "sal_btn": "Calcular Rentabilidad Clinica", "sal_res1": "Ingresos Brutos Estimados: ${:.2f}", "sal_res2": "Ganancia Neta Estimada: ${:.2f}",
        "con_sub": "Sector Construccion (Calculo de Presupuesto por m2)", "con_m": "Metros cuadrados (m2):", "con_c": "Costo de materiales por m2 ($):", "con_o": "Costo de mano de obra por m2 ($):", "con_btn": "Calcular Presupuesto Obra", "con_res1": "Presupuesto Total Estimado: ${:.2f}", "con_res2": "Costo Total por m2: ${:.2f}",
        "fin_sub": "Sector Finanzas (Calculo de Interes Compuesto / ROI)", "fin_cap": "Capital inicial ($):", "fin_tasa": "Tasa anual (%):", "fin_anos": "Anos de inversion:", "fin_btn": "Calcular Rendimiento", "fin_res1": "Monto Final Estimado: ${:.2f}", "fin_res2": "Ganancia Total: ${:.2f}",
        "edu_sub": "Sector Educacion (Calculo de Costo por Alumno)", "edu_al": "Numero de alumnos:", "edu_cur": "Costo operativo del curso ($):", "edu_mat": "Costo material por alumno ($):", "edu_btn": "Calcular Costo Educativo", "edu_res1": "Costo Total del Programa: ${:.2f}", "edu_res2": "Costo por Alumno: ${:.2f}",
        "hist_titulo": "Tabla de Registros (1 minimo / 25 maximo)", "hist_vacio": "Aun no hay registros.", "btn_borrar": "Borrar todas las tablas"
    },
    "English": {
        "titulo": "Interactive Sector Calculator",
        "descripcion": "Select a sector, enter data, and calculate results automatically.",
        "lbl_sector": "Choose the economic sector:",
        "sectores": ["Technology / Software","Manufacturing","Retail / Commerce","Healthcare / Clinic","Construction / Building","Finance / Investment","Education / Training"],
        "btn_cambiar_idioma": "Cambiar a Espanol",
        "tech_sub": "Technology Sector (SaaS / Licensing Calculation)", "tech_u": "Number of active users:", "tech_c": "Monthly cost per user ($):", "tech_d": "Applied discount (%):", "tech_btn": "Calculate Total", "tech_res": "Total Monthly Cost: ${:.2f}",
        "man_sub": "Manufacturing Sector (Production Calculation)", "man_u": "Units to produce:", "man_m": "Material cost per unit ($):", "man_f": "Fixed operational costs ($):", "man_btn": "Calculate Production Cost", "man_res1": "Total Production Cost: ${:.2f}", "man_res2": "Cost per manufactured unit: ${:.2f}",
        "com_sub": "Retail Sector (Margin & Sale Calculation)", "com_c": "Product acquisition cost ($):", "com_m": "Desired profit margin (%):", "com_i": "Local tax / VAT (%):", "com_btn": "Calculate Selling Price", "com_res1": "Public Retail Price: ${:.2f}", "com_res2": "Net profit per product: ${:.2f}",
        "sal_sub": "Healthcare Sector (Consultation & Procedure Calculation)", "sal_c": "Estimated number of consultations:", "sal_p": "Base price per consultation ($):", "sal_o": "Operating cost per consultation ($):", "sal_btn": "Calculate Clinic Profitability", "sal_res1": "Estimated Gross Revenue: ${:.2f}", "sal_res2": "Estimated Net Profit: ${:.2f}",
        "con_sub": "Construction Sector (Budget per m2 Calculation)", "con_m": "Square meters (m2):", "con_c": "Material cost per m2 ($):", "con_o": "Labor cost per m2 ($):", "con_btn": "Calculate Construction Budget", "con_res1": "Total Estimated Budget: ${:.2f}", "con_res2": "Total Cost per m2: ${:.2f}",
        "fin_sub": "Finance Sector (Compound Interest / ROI Calculation)", "fin_cap": "Initial capital ($):", "fin_tasa": "Annual rate (%):", "fin_anos": "Years of investment:", "fin_btn": "Calculate Yield", "fin_res1": "Estimated Final Amount: ${:.2f}", "fin_res2": "Total Profit: ${:.2f}",
        "edu_sub": "Education Sector (Cost per Student Calculation)", "edu_al": "Number of students:", "edu_cur": "Course operating cost ($):", "edu_mat": "Material cost per student ($):", "edu_btn": "Calculate Educational Cost", "edu_res1": "Total Program Cost: ${:.2f}", "edu_res2": "Cost per Student: ${:.2f}",
        "hist_titulo": "Records Table (1 min / 25 max)", "hist_vacio": "No records yet.", "btn_borrar": "Clear all tables"
    }
}

txt = TEXTOS[st.session_state.idioma]
st.markdown(f'<div class="header-card"><div class="header-title">{txt["titulo"]}</div><div class="header-subtitle">{txt["descripcion"]}</div></div>', unsafe_allow_html=True)

sector = st.selectbox(txt["lbl_sector"], txt["sectores"])

if st.button(txt["btn_cambiar_idioma"]):
    st.session_state.idioma = "English" if st.session_state.idioma == "Español" else "Español"
    st.rerun()

st.divider()

if sector in ["Tecnologia / Software", "Technology / Software"]:
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
elif sector in ["Salud / Clinica", "Healthcare / Clinic"]:
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
elif sector in ["Construccion / Obras", "Construction / Building"]:
    st.subheader(txt["con_sub"])
    metros = st.number_input(txt["con_m"], min_value=1.0, value=150.0, step=10.0)
    costo_material_m2 = st.number_input(txt["con_c"], min_value=0.0, value=120.0, step=5.0)
    costo_obra_m2 = st.number_input(txt["con_o"], min_value=0.0, value=80.0, step=5.0)
    if st.button(txt["con_btn"]):
        costo_m2_total = costo_material_m2 + costo_obra_m2
        total = metros * costo_m2_total
        st.success(txt["con_res1"].format(total))
        st.info(txt["con_res2"].format(costo_m2_total))
        guardar_en_tabla(sector, f"{metros} m2 x (${costo_material_m2}+${costo_obra_m2})", f"${total:.2f}")
elif sector in ["Finanzas / Inversion", "Finance / Investment"]:
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
elif sector in ["Educacion / Formacion", "Education / Training"]:
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
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(txt["btn_borrar"]):
            st.session_state.historial = []
            st.rerun()
    with col2:
        excel_data, ext, mime = generar_excel(df)
        label = "Descargar Excel" if ext == "xlsx" else "Descargar CSV"
        st.download_button(label=label, data=excel_data, file_name=f"registros_calculadora.{ext}", mime=mime, use_container_width=True)
    with col3:
        pdf_data = generar_pdf(df)
        st.download_button(label="Descargar PDF", data=pdf_data, file_name="registros_calculadora.pdf", mime="application/pdf", use_container_width=True)
else:
    st.info(txt["hist_vacio"]) 
