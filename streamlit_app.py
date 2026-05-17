import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta
from supabase import create_client, Client

# ─────────────────────────────────────────
# CONEXIÓN SUPABASE
# ─────────────────────────────────────────
@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_supabase()

# ─────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Gestión Biomédica SPORTMEDS",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# ESTILOS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');
* { font-family: 'DM Sans', sans-serif !important; }

.main .block-container { background-color: #ffffff !important; padding-top: 1.2rem !important; max-width: 100% !important; }
.main { background-color: #ffffff !important; }
[data-testid="stAppViewContainer"] { background-color: #ffffff !important; }
[data-testid="stAppViewBlockContainer"] { background-color: #ffffff !important; }
section.main { background-color: #ffffff !important; }

section[data-testid="stSidebar"] { background: white !important; border-right: 1px solid #e8edf5 !important; }
section[data-testid="stSidebar"] * { color: #0D2B52 !important; }
section[data-testid="stSidebar"] .stSelectbox > div > div { background: #F0F4F9 !important; border: 1px solid #dce5f0 !important; border-radius: 8px !important; }
section[data-testid="stSidebar"] label { font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 0.08em; color: #8a9bb5 !important; }
section[data-testid="stSidebar"] hr { border-color: #e8edf5 !important; margin: 0.6rem 0 !important; }
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 { color: #0D2B52 !important; font-size: 0.95rem !important; }

.topbar { display:flex; align-items:center; justify-content:space-between; background:white; border-radius:10px; padding:0.65rem 1.2rem; margin-bottom:1rem; box-shadow:0 2px 12px rgba(13,43,82,0.09); }
.topbar-title { font-size:1.05rem; font-weight:700; color:#0D2B52; }
.topbar-crumb { font-size:0.72rem; color:#8a9bb5; margin-top:1px; }
.topbar-user  { font-size:0.83rem; font-weight:600; color:#0D2B52; }

.kpi-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:1rem; }
.kpi-card { background:white; border-radius:12px; padding:1rem 1.1rem; box-shadow:0 2px 12px rgba(13,43,82,0.09); display:flex; align-items:center; gap:0.9rem; border-top:3px solid #1a8fd1; transition:transform .15s; }
.kpi-card:hover { transform:translateY(-2px); }
.kpi-icon { font-size:1.7rem; background:rgba(26,143,209,0.1); border-radius:10px; width:50px; height:50px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.kpi-val   { font-size:1.55rem; font-weight:700; color:#0D2B52; line-height:1; }
.kpi-label { font-size:0.75rem; color:#8a9bb5; margin-top:3px; }
.kpi-delta { font-size:0.7rem; margin-top:3px; }
.up   { color:#27ae60; }
.down { color:#e74c3c; }

.card { background:white; border-radius:12px; padding:1rem 1.1rem 0.6rem; box-shadow:0 2px 12px rgba(13,43,82,0.09); }
.card-title { font-size:0.88rem; font-weight:700; color:#0D2B52; border-bottom:1px solid #eef2f7; padding-bottom:0.4rem; margin-bottom:0.5rem; }

.seccion-header { background: linear-gradient(135deg, #0D2B52, #1a8fd1); color: white !important; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 700; font-size: 0.9rem; margin: 1rem 0 0.5rem 0; }

.stButton > button { background:linear-gradient(135deg,#0D2B52,#1a8fd1) !important; color:white !important; border:none !important; border-radius:8px !important; font-weight:600 !important; }
.stButton > button:hover { opacity:0.85 !important; }
.stTextInput input, .stTextArea textarea { border-radius:8px !important; border:1px solid #dce5f0 !important; }

.main .stTextInput label, .main .stTextArea label, .main .stSelectbox label,
.main .stNumberInput label, .main .stDateInput label, .main .stSlider label,
.main .stMarkdown p, .main h4, .main h3, .main h2,
[data-testid="stForm"] label, [data-testid="stForm"] p { color:#0D2B52 !important; font-weight:500 !important; }

[data-testid="stTabs"] button { color:#8a9bb5 !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color:#0D2B52 !important; font-weight:700 !important; }

.npr-box { border-radius:10px; padding:1rem; text-align:center; margin-top:0.8rem; }

.badge-serio    { background:#fde8e8; color:#c0392b; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }
.badge-noserio  { background:#fef9e7; color:#b7770d; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }
.badge-ok       { background:#eafaf1; color:#1e8449; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }

#MainMenu { visibility:hidden; }
footer    { visibility:hidden; }

[data-testid="collapsedControl"] { background:#0D2B52 !important; border-radius:0 10px 10px 0 !important; padding:14px 10px !important; box-shadow:3px 0 12px rgba(0,0,0,0.25) !important; overflow:hidden !important; width:44px !important; display:flex !important; align-items:center !important; justify-content:center !important; }
[data-testid="collapsedControl"]:hover { background:#1a8fd1 !important; }
[data-testid="collapsedControl"] svg, [data-testid="collapsedControl"] span { display:none !important; }
[data-testid="collapsedControl"]::after { content:""; display:block; width:22px; height:2px; background:white; border-radius:2px; box-shadow:0 7px 0 white,0 14px 0 white; margin:0 auto; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# RUTAS
# ─────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "assets", "Logo_sportmeds.png")

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, width=190)
else:
    st.sidebar.markdown("<div style='font-size:1.1rem;font-weight:700;'>⚕️ SPORTMEDS</div>", unsafe_allow_html=True)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("### Menú Principal")

modulo = st.sidebar.selectbox(
    "Seleccione un módulo",
    [
        "🏠  Panel de Control",
        "📦  Inventario",
        "🔍  Tecnovigilancia",
        "📁  Casos Reportados",
        "⚠️  Gestión de Riesgos",
        "🔧  Mantenimiento",
    ]
)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style='padding:0.2rem 0;'>
    <div style='font-size:0.67rem;color:rgba(13,43,82,0.5);text-transform:uppercase;letter-spacing:.08em;'>Usuario</div>
    <div style='font-size:0.9rem;font-weight:600;margin-top:3px;'>Ing. Biomédico</div>
    <div style='font-size:0.7rem;color:rgba(13,43,82,0.45);'>Administrador</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<div style='font-size:0.65rem;color:rgba(13,43,82,0.35);text-align:center;'>"
    "Gestión Biomédica v1.0<br>© 2025 SPORTMEDS Centro Médico</div>",
    unsafe_allow_html=True
)

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
PLOT_CFG = {"displayModeBar": False}

def base_layout(h=220):
    return dict(height=h, margin=dict(l=0,r=0,t=4,b=0), plot_bgcolor="white", paper_bgcolor="white")

def topbar(titulo, ruta):
    st.markdown(f"""
    <div class="topbar">
        <div><div class="topbar-title">{titulo}</div><div class="topbar-crumb">INICIO › {ruta}</div></div>
        <div class="topbar-user">👤 Ing. Biomédico &nbsp;🔒</div>
    </div>""", unsafe_allow_html=True)

def seccion(titulo):
    st.markdown(f'<div class="seccion-header">{titulo}</div>', unsafe_allow_html=True)

# Causas NTC 5736:2009
CAUSAS_NTC = [
    "930 — Sin identificar (en investigación)",
    "500 — Uso anormal",
    "510 — Respuesta fisiológica anormal o inesperada",
    "520 — Falla en la alarma",
    "530 — Uso de material biológico",
    "540 — Calibración incorrecta",
    "550 — Hardware del computador",
    "560 — Contaminación durante la producción",
    "570 — Contaminación post-producción",
    "580 — Diseño inadecuado",
    "590 — Desconexión",
    "600 — Componente eléctrico",
    "610 — Circuito eléctrico",
    "620 — Contacto eléctrico",
    "630 — Interferencia Electromagnética (IEM)",
    "640 — Fecha de expiración",
    "650 — Falso Negativo",
    "660 — Falso Positivo",
    "670 — Resultado falso de la prueba",
    "680 — Falla en el dispositivo implantable",
    "690 — Ambiente inapropiado",
    "700 — Incompatibilidad",
    "710 — Instrucciones para uso y etiquetado",
    "720 — Escape / sellado",
    "730 — Mantenimiento inadecuado",
    "740 — Fabricación",
    "750 — Material",
    "760 — Componentes mecánicos",
    "770 — Condiciones no higiénicas",
    "780 — No relacionado con el dispositivo",
    "790 — Otros",
    "800 — Empaque",
    "810 — Anatomía / Fisiología del paciente",
    "820 — Condición del paciente",
    "830 — Fuente de energía",
    "840 — Medidas de protección",
    "850 — Aseguramiento de calidad institucional",
    "860 — Radiación",
    "870 — Software",
    "880 — Esterilización / desinfección / limpieza",
    "890 — Condiciones de almacenamiento",
    "900 — Alteración, falsificación, sabotaje",
    "910 — Entrenamiento inadecuado",
    "920 — Transporte y entrega",
    "940 — Capacidad de Uso",
    "950 — Error de Uso",
    "960 — Desgaste",
]

# ══════════════════════════════════════════
# PANEL DE CONTROL
# ══════════════════════════════════════════
if "Panel" in modulo:
    topbar("Panel de Control", "Panel de Control")

    try:
        inv_data = supabase.table("Inventario").select("*").execute().data
        df_inv   = pd.DataFrame(inv_data) if inv_data else pd.DataFrame()
        total_equipos  = len(df_inv)
        riesgo_alto    = len(df_inv[df_inv["clase_riesgo"]=="Clase III"]) if not df_inv.empty and "clase_riesgo" in df_inv.columns else 0
        fuera_servicio = len(df_inv[df_inv["estado"].str.contains("Fuera", na=False)]) if not df_inv.empty and "estado" in df_inv.columns else 0
    except:
        total_equipos = riesgo_alto = fuera_servicio = 0
        df_inv = pd.DataFrame()

    try:
        tv_data  = supabase.table("Tecnovigilancia").select("id,clasificacion").execute().data
        total_tv = len(tv_data) if tv_data else 0
        tv_serios = len([r for r in tv_data if r.get("clasificacion","") and "serio" in r.get("clasificacion","").lower()]) if tv_data else 0
    except:
        total_tv = tv_serios = 0

    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-icon">🩺</div>
        <div><div class="kpi-val">{total_equipos}</div><div class="kpi-label">Equipos registrados</div><div class="kpi-delta up">Base de datos activa</div></div>
      </div>
      <div class="kpi-card" style="border-top-color:#e74c3c;">
        <div class="kpi-icon" style="background:rgba(231,76,60,.1);">⚠️</div>
        <div><div class="kpi-val">{riesgo_alto}</div><div class="kpi-label">Equipos Clase III</div><div class="kpi-delta down">Riesgo alto</div></div>
      </div>
      <div class="kpi-card" style="border-top-color:#e67e22;">
        <div class="kpi-icon" style="background:rgba(230,126,34,.1);">🔧</div>
        <div><div class="kpi-val">{fuera_servicio}</div><div class="kpi-label">Fuera de servicio</div><div class="kpi-delta" style="color:#e67e22;">● Requieren atención</div></div>
      </div>
      <div class="kpi-card" style="border-top-color:#9b59b6;">
        <div class="kpi-icon" style="background:rgba(155,89,182,.1);">📋</div>
        <div><div class="kpi-val">{total_tv}</div><div class="kpi-label">Eventos tecnovigilancia</div><div class="kpi-delta {'down' if tv_serios>0 else 'up'}">{tv_serios} serios</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.4,1.1,1.4])
    with c1:
        st.markdown('<div class="card"><div class="card-title">Equipos por estado</div>', unsafe_allow_html=True)
        if not df_inv.empty and "estado" in df_inv.columns:
            ec = df_inv["estado"].value_counts()
            fig = go.Figure(go.Bar(x=ec.index.tolist(), y=ec.values.tolist(),
                marker_color=["#27ae60" if "En servicio" in e else "#e74c3c" for e in ec.index],
                text=ec.values.tolist(), textposition="outside"))
        else:
            fig = go.Figure(go.Bar(x=["Sin datos"], y=[0], marker_color="#8a9bb5"))
        lay = base_layout(); lay.update(xaxis=dict(showgrid=False,tickfont_size=9), yaxis=dict(gridcolor="#f0f4f9"))
        fig.update_layout(lay); st.plotly_chart(fig, use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><div class="card-title">Equipos por clase INVIMA</div>', unsafe_allow_html=True)
        if not df_inv.empty and "clase_riesgo" in df_inv.columns:
            cc = df_inv["clase_riesgo"].value_counts()
            fig2 = go.Figure(go.Pie(labels=cc.index.tolist(), values=cc.values.tolist(), hole=0.52,
                marker_colors=["#27ae60","#1a8fd1","#e67e22","#e74c3c"], textfont_size=10))
        else:
            fig2 = go.Figure(go.Pie(labels=["Sin datos"], values=[1], hole=0.52, marker_colors=["#8a9bb5"]))
        fig2.update_layout(height=220, margin=dict(l=0,r=0,t=4,b=0), paper_bgcolor="white",
            showlegend=True, legend=dict(orientation="h", y=-0.28, font_size=9))
        st.plotly_chart(fig2, use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="card"><div class="card-title">Equipos por servicio</div>', unsafe_allow_html=True)
        if not df_inv.empty and "servicio" in df_inv.columns:
            sc = df_inv["servicio"].value_counts()
            fig3 = go.Figure(go.Bar(x=sc.values.tolist(), y=sc.index.tolist(), orientation="h",
                marker_color="#1a8fd1", text=sc.values.tolist(), textposition="outside"))
        else:
            fig3 = go.Figure(go.Bar(x=[0], y=["Sin datos"], orientation="h", marker_color="#8a9bb5"))
        lay3 = base_layout(); lay3.update(xaxis=dict(showgrid=False,visible=False), yaxis=dict(showgrid=False,tickfont_size=10))
        fig3.update_layout(lay3); st.plotly_chart(fig3, use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c4, c5 = st.columns([1.6,1])
    with c4:
        st.markdown('<div class="card"><div class="card-title">Eventos tecnovigilancia — últimos 30 días</div>', unsafe_allow_html=True)
        dias = [(date.today()-timedelta(days=i)).strftime("%Y-%m-%d") for i in range(29,-1,-1)]
        dias_label = [(date.today()-timedelta(days=i)).strftime("%d/%m") for i in range(29,-1,-1)]
        try:
            tv_todos = supabase.table("Tecnovigilancia").select("fecha_evento").execute().data
            conteo = {d:0 for d in dias}
            if tv_todos:
                for row in tv_todos:
                    f = row.get("fecha_evento","")
                    if f and f[:10] in conteo: conteo[f[:10]] += 1
            valores = list(conteo.values())
        except:
            valores = [0]*30
        fig4 = go.Figure(go.Scatter(x=dias_label, y=valores, mode="lines+markers",
            line=dict(color="#1a8fd1",width=2), marker=dict(color="#0D2B52",size=5),
            fill="tozeroy", fillcolor="rgba(26,143,209,0.07)"))
        lay4 = base_layout(210); lay4.update(xaxis=dict(showgrid=False,tickangle=-45,tickfont_size=8,
            tickvals=dias_label[::5],ticktext=dias_label[::5]), yaxis=dict(gridcolor="#f0f4f9",tickfont_size=10,dtick=1))
        fig4.update_layout(lay4); st.plotly_chart(fig4, use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    with c5:
        st.markdown('<div class="card"><div class="card-title">Últimos equipos registrados</div>', unsafe_allow_html=True)
        if not df_inv.empty:
            cols = ["numero_inventario","descripcion","servicio","estado"]
            cols_ok = [c for c in cols if c in df_inv.columns]
            st.dataframe(df_inv[cols_ok].tail(5), use_container_width=True, hide_index=True, height=210)
        else:
            st.info("Sin registros aún.")
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# INVENTARIO
# ══════════════════════════════════════════
elif "Inventario" in modulo:
    topbar("Inventario Biomédico", "Inventario")
    tab1, tab2 = st.tabs(["➕  Registrar equipo","📋  Listado de equipos"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("form_inv", clear_on_submit=True):
            seccion("🔖 Identificación del equipo")
            c1,c2,c3 = st.columns(3)
            with c1:
                numero_inventario = st.text_input("N° de inventario *")
                tipo_equipo = st.selectbox("Tipo de equipo *",["Equipo de diagnóstico por imagen","Equipo de monitoreo","Equipo de soporte vital","Equipo de laboratorio","Equipo quirúrgico","Equipo de rehabilitación","Otro"])
                descripcion = st.text_input("Descripción del equipo *")
            with c2:
                fabricante   = st.text_input("Fabricante *")
                modelo       = st.text_input("Modelo / N° catálogo")
                numero_serie = st.text_input("N° de serie")
            with c3:
                numero_lote  = st.text_input("N° de lote")
                clase_riesgo = st.selectbox("Clase de riesgo INVIMA",["Clase I","Clase IIa","Clase IIb","Clase III"])
                alimentacion = st.selectbox("Alimentación eléctrica",["110V","220V","380V","Trifásica","No aplica"])

            seccion("📍 Ubicación y estado")
            c4,c5,c6 = st.columns(3)
            with c4:
                servicio  = st.selectbox("Servicio *",["UCI","Urgencias","Hospitalización","Consulta externa","Imágenes diagnósticas","Cirugía","Laboratorio","Rehabilitación"])
                ubicacion = st.text_input("Habitación / Área específica")
            with c5:
                estado    = st.selectbox("Estado operativo *",["En servicio","Fuera de servicio - Mantenimiento preventivo","Fuera de servicio - En reparación","Fuera de servicio - Pendiente calibración","Fuera de servicio - Dado de baja"])
                requisitos= st.text_input("Requisitos especiales")
            with c6:
                proveedor_compra = st.text_input("Proveedor de compra")
                proveedor_mant   = st.text_input("Proveedor de mantenimiento")

            seccion("📅 Fechas y costos")
            c7,c8,c9 = st.columns(3)
            with c7:
                fecha_compra   = st.date_input("Fecha de compra",   value=date.today())
                fecha_registro = st.date_input("Fecha de registro",  value=date.today())
            with c8:
                garantia_inicio = st.date_input("Garantía inicio", value=date.today())
                garantia_fin    = st.date_input("Garantía fin",    value=date.today())
            with c9:
                costo     = st.number_input("Costo (COP)", min_value=0, step=100000)
                vida_util = st.number_input("Vida útil (años)", 1, 30, 5)
            obs = st.text_area("Observaciones adicionales")

            if st.form_submit_button("✅ Registrar equipo en base de datos", use_container_width=True):
                if numero_inventario and descripcion and fabricante:
                    try:
                        supabase.table("Inventario").insert({
                            "numero_inventario": numero_inventario, "tipo_equipo": tipo_equipo,
                            "descripcion": descripcion, "fabricante": fabricante, "modelo": modelo,
                            "numero_serie": numero_serie, "numero_lote": numero_lote,
                            "clase_riesgo": clase_riesgo, "alimentacion_electrica": alimentacion,
                            "servicio": servicio, "Ubicación": ubicacion, "estado": estado,
                            "proveedor_compra": proveedor_compra, "proveedor_mantenimiento": proveedor_mant,
                            "fecha_compra": str(fecha_compra), "fecha_registro": str(fecha_registro),
                            "garantia_inicio": str(garantia_inicio), "garantia_fin": str(garantia_fin),
                            "costo": float(costo), "observaciones": obs,
                        }).execute()
                        st.success(f"✅ **{descripcion}** registrado correctamente.")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error al guardar: {e}")
                else:
                    st.error("Complete los campos obligatorios (*).")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card"><div class="card-title">Equipos registrados</div>', unsafe_allow_html=True)
        try:
            resp = supabase.table("Inventario").select("*").execute()
            if resp.data:
                df = pd.DataFrame(resp.data)
                cols_show = ["numero_inventario","descripcion","fabricante","modelo","clase_riesgo","servicio","estado","fecha_compra"]
                cols_ok = [c for c in cols_show if c in df.columns]
                st.dataframe(df[cols_ok], use_container_width=True, hide_index=True)
                st.download_button("📥 Exportar a CSV", df.to_csv(index=False).encode("utf-8"), "inventario_sportmeds.csv","text/csv")
            else:
                st.info("No hay equipos registrados aún.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# TECNOVIGILANCIA — FOREIA001
# ══════════════════════════════════════════
elif "Tecnovigilancia" in modulo:
    topbar("Tecnovigilancia — FOREIA001", "Tecnovigilancia")

    @st.cache_data(ttl=60)
    def cargar_inventario():
        try:
            data = supabase.table("Inventario").select("*").execute().data
            return pd.DataFrame(data) if data else pd.DataFrame()
        except:
            return pd.DataFrame()

    df_inv = cargar_inventario()

    st.markdown('<div class="card"><div class="card-title">🔍 Selección del equipo involucrado</div>', unsafe_allow_html=True)
    if df_inv.empty:
        st.warning("⚠️ No hay equipos en el inventario. Registra equipos primero.")
        equipo_sel = None
    else:
        opciones = ["— Seleccione un equipo —"] + [
            f"{row['numero_inventario']} — {row['descripcion']} ({row.get('fabricante','')}) · {row.get('servicio','')}"
            for _, row in df_inv.iterrows()
        ]
        equipo_label = st.selectbox("Equipo involucrado en el evento *", opciones,
            help="Al seleccionar, los datos técnicos se llenan automáticamente.")
        equipo_sel = None
        if equipo_label != "— Seleccione un equipo —":
            inv_id  = equipo_label.split(" — ")[0].strip()
            matches = df_inv[df_inv["numero_inventario"] == inv_id]
            if not matches.empty:
                equipo_sel = matches.iloc[0]
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("form_foreia001", clear_on_submit=True):

        # SECCIÓN A
        seccion("🏥 A. Lugar de ocurrencia del evento o incidente")
        ca1,ca2,ca3 = st.columns(3)
        with ca1:
            st.text_input("A1. Nombre de la institución", value="SPORTMEDS Centro Médico S.A.S", disabled=True)
            st.text_input("A4. NIT", value="901.002.107-7", disabled=True)
        with ca2:
            st.text_input("A2. Departamento", value="Valle del Cauca", disabled=True)
            st.text_input("A5. Nivel de complejidad", value="2", disabled=True)
        with ca3:
            st.text_input("A3. Ciudad", value="Cali", disabled=True)
            st.text_input("A6. Naturaleza", value="Privada", disabled=True)

        # SECCIÓN B
        seccion("🧑‍⚕️ B. Información del paciente")
        cb1,cb2,cb3,cb4 = st.columns([1.2,0.8,0.8,1.5])
        with cb1:
            pac_id = st.text_input("B1. Identificación del paciente *", placeholder="Iniciales o N° historia clínica")
        with cb2:
            pac_sexo = st.selectbox("B2. Sexo *", ["— Seleccione —","Femenino","Masculino"])
        with cb3:
            pac_edad = st.text_input("B3. Edad *", placeholder="ej. 45 años")
        with cb4:
            pac_dx = st.text_input("B4. Diagnóstico inicial *", placeholder="Causa de atención que originó el uso del DM")

        # SECCIÓN C
        seccion("🩺 C. Identificación del dispositivo médico")
        st.caption("Campos llenados automáticamente desde el inventario — no editables.")

        if equipo_sel is not None:
            nombre_generico  = str(equipo_sel.get("descripcion","") or "")
            nombre_comercial = str(equipo_sel.get("modelo","") or "")
            registro_san     = str(equipo_sel.get("clase_riesgo","") or "")
            lote_val         = str(equipo_sel.get("numero_lote","") or "")
            modelo_val       = str(equipo_sel.get("modelo","") or "")
            serial_val       = str(equipo_sel.get("numero_serie","") or "")
            fabricante_val   = str(equipo_sel.get("fabricante","") or "")
            importador_val   = str(equipo_sel.get("proveedor_compra","") or "")
            area_val         = str(equipo_sel.get("servicio","") or "")
            num_inv_val      = str(equipo_sel.get("numero_inventario","") or "")
        else:
            nombre_generico = nombre_comercial = registro_san = lote_val = ""
            modelo_val = serial_val = fabricante_val = importador_val = area_val = num_inv_val = ""

        cc1,cc2 = st.columns(2)
        with cc1:
            st.text_input("C1. Nombre genérico del dispositivo médico", value=nombre_generico, disabled=True)
            st.text_input("C3. Registro sanitario / Clase de riesgo",   value=registro_san,    disabled=True)
            st.text_input("C5. Fabricante",                              value=fabricante_val,  disabled=True)
            st.text_input("C7. Área de funcionamiento",                  value=area_val,        disabled=True)
        with cc2:
            st.text_input("C2. Nombre comercial",  value=nombre_comercial, disabled=True)
            cl1,cl2 = st.columns(2)
            with cl1: st.text_input("C4. Lote",    value=lote_val,  disabled=True)
            with cl2: st.text_input("Modelo",      value=modelo_val, disabled=True)
            cr1,cr2 = st.columns(2)
            with cr1: st.text_input("Referencia",  value=modelo_val,  disabled=True)
            with cr2: st.text_input("Serial",      value=serial_val,  disabled=True)
            st.text_input("C6. Importador / Distribuidor", value=importador_val, disabled=True)
            uso_multiple = st.radio("C8. ¿Dispositivo utilizado más de una vez?", ["No","Sí"], horizontal=True)

        # SECCIÓN D
        seccion("⚠️ D. Evento o incidente adverso")
        cd1,cd2,cd3 = st.columns(3)
        with cd1:
            fecha_evento  = st.date_input("D1. Fecha del evento *", value=date.today())
        with cd2:
            st.text_input("D2. Fecha de elaboración del reporte", value=date.today().strftime("%d/%m/%Y"), disabled=True)
        with cd3:
            deteccion = st.selectbox("D3. Detección del evento",["Antes del uso del dispositivo médico","Durante el uso del dispositivo médico","Después del uso del dispositivo médico"])

        clasificacion = st.radio("D4. Clasificación *",
            ["Evento adverso serio","Evento adverso no serio","Incidente adverso serio","Incidente adverso no serio"],
            horizontal=True)

        descripcion_ev = st.text_area("D5. Descripción detallada del evento *", height=130,
            placeholder="Describa: estado de salud del paciente, signos y síntomas, antecedentes, curso clínico, tratamiento...")

        st.markdown("**D6. Desenlace del evento** — seleccione todas las que apliquen:")
        dc1,dc2,dc3 = st.columns(3)
        with dc1:
            d_muerte  = st.checkbox("Muerte")
            d_amenaza = st.checkbox("Enfermedad o daño que amenace la vida")
        with dc2:
            d_funcion = st.checkbox("Daño de una función o estructura corporal")
            d_hosp    = st.checkbox("Hospitalización inicial o prolongada")
        with dc3:
            d_interv  = st.checkbox("Requiere intervención médica o quirúrgica")
            d_sin     = st.checkbox("No hubo daño")
            d_otro    = st.checkbox("Otro")
        d_otro_cual = st.text_input("Especifique el otro desenlace:") if d_otro else ""

        # SECCIÓN E
        seccion("📋 E. Gestión realizada")
        ce1,ce2 = st.columns(2)
        with ce1:
            causa_codigo = st.selectbox(
                "E1. Causa probable del evento (código NTC 5736:2009) *",
                CAUSAS_NTC,
                help="Seleccione el código que mejor describe la causa probable. Puede actualizar después de la investigación."
            )
            causa_descripcion = st.text_area("E1. Descripción de la causa probable", height=80,
                placeholder="Describa con detalle la causa identificada del evento o incidente...")
            acciones = st.text_area("E2. Acciones correctivas y preventivas iniciadas", height=80,
                placeholder="Describa las acciones tomadas para corregir y prevenir recurrencia...")
        with ce2:
            reporto_imp = st.radio("E3. ¿Reportó al importador/distribuidor?", ["No","Sí"], horizontal=True)
            fecha_rep_imp = None
            if reporto_imp == "Sí":
                fecha_rep_imp = st.date_input("E3. Fecha de reporte al importador", value=date.today())
            disp_disponible = st.radio("E4. ¿Dispositivo médico disponible para evaluación?", ["Sí","No"], horizontal=True,
                help="No enviar al INVIMA — disponible para evaluación del fabricante")
            disp_enviado = st.radio("E5. ¿Se ha enviado el dispositivo al distribuidor/importador?", ["No","Sí"], horizontal=True)
            fecha_envio_disp = None
            if disp_enviado == "Sí":
                fecha_envio_disp = st.date_input("E5. Fecha de envío del dispositivo", value=date.today())

        # SECCIÓN F
        seccion("👤 F. Información del reportante")
        cf1,cf2,cf3 = st.columns(3)
        with cf1:
            rep_nombre = st.text_input("F1. Nombre completo *")
            rep_prof   = st.text_input("F2. Profesión *", placeholder="ej. Médico, Enfermero, Ing. Biomédico")
            rep_org    = st.text_input("F3. Organización o área a la que pertenece")
        with cf2:
            rep_dir   = st.text_input("F4. Dirección de la organización")
            rep_tel   = st.text_input("F5. Teléfono de contacto")
            rep_depto = st.text_input("F6. Departamento", value="Valle del Cauca")
        with cf3:
            rep_ciudad = st.text_input("F7. Ciudad", value="Cali")
            rep_email  = st.text_input("F8. Correo electrónico institucional")
            fecha_noti = st.date_input("F9. Fecha de notificación", value=date.today())
            autoriza   = st.radio("F10. ¿Autoriza divulgación del origen del reporte?", ["No","Sí"], horizontal=True)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("📋 Guardar reporte FOREIA001 en base de datos", use_container_width=True)

        if submitted:
            errores = []
            if equipo_sel is None:         errores.append("Debe seleccionar un equipo del inventario.")
            if not pac_id:                 errores.append("La identificación del paciente es obligatoria (B1).")
            if pac_sexo == "— Seleccione —": errores.append("El sexo del paciente es obligatorio (B2).")
            if not pac_edad:               errores.append("La edad del paciente es obligatoria (B3).")
            if not pac_dx:                 errores.append("El diagnóstico inicial es obligatorio (B4).")
            if not descripcion_ev:         errores.append("La descripción del evento es obligatoria (D5).")
            if not causa_descripcion:      errores.append("La causa probable es obligatoria (E1).")
            if not acciones:               errores.append("Las acciones correctivas son obligatorias (E2).")
            if not rep_nombre:             errores.append("El nombre del reportante es obligatorio (F1).")
            if not rep_prof:               errores.append("La profesión del reportante es obligatoria (F2).")

            if errores:
                for e in errores: st.error(f"❌ {e}")
            else:
                desenlaces = []
                if d_muerte:  desenlaces.append("Muerte")
                if d_amenaza: desenlaces.append("Enfermedad o daño que amenace la vida")
                if d_funcion: desenlaces.append("Daño de una función o estructura corporal")
                if d_hosp:    desenlaces.append("Hospitalización inicial o prolongada")
                if d_interv:  desenlaces.append("Requiere intervención médica o quirúrgica")
                if d_sin:     desenlaces.append("No hubo daño")
                if d_otro:    desenlaces.append(f"Otro: {d_otro_cual}")

                try:
                    supabase.table("Tecnovigilancia").insert({
                        # A
                        "nombre_institucion": "SPORTMEDS Centro Médico",
                        "departamento": "Valle del Cauca", "ciudad": "Cali",
                        "nit": "901.002.107-7", "nivel_complejidad": "2", "naturaleza": "Privada",
                        # B
                        "paciente_identificacion": pac_id, "paciente_sexo": pac_sexo,
                        "paciente_edad": pac_edad, "paciente_diagnostico": pac_dx,
                        # C
                        "numero_inventario": num_inv_val, "nombre_generico": nombre_generico,
                        "nombre_comercial": nombre_comercial, "registro_sanitario": registro_san,
                        "lote": lote_val, "modelo": modelo_val, "referencia": modelo_val,
                        "serial": serial_val, "fabricante": fabricante_val, "importador": importador_val,
                        "area_funcionamiento": area_val, "uso_multiple_texto": uso_multiple,
                        # D
                        "fecha_evento": str(fecha_evento),
                        "fecha_elaboracion_reporte": str(date.today()),
                        "deteccion": deteccion, "clasificacion": clasificacion,
                        "descripcion_evento": descripcion_ev,
                        "desenlace": desenlaces, "desenlace_otro": d_otro_cual,
                        # E
                        "causa_probable": causa_descripcion,
                        "causa_codigo": causa_codigo.split(" — ")[0],
                        "acciones_correctivas": acciones,
                        "reporto_importador": reporto_imp == "Sí",
                        "fecha_reporte_importador": str(fecha_rep_imp) if fecha_rep_imp else None,
                        "dispositivo_disponible": disp_disponible == "Sí",
                        "dispositivo_enviado": disp_enviado == "Sí",
                        "fecha_envio_dispositivo": str(fecha_envio_disp) if fecha_envio_disp else None,
                        # F
                        "reportante_nombre": rep_nombre, "reportante_profesion": rep_prof,
                        "reportante_organizacion": rep_org, "reportante_direccion": rep_dir,
                        "reportante_telefono": rep_tel, "reportante_departamento": rep_depto,
                        "reportante_ciudad": rep_ciudad, "reportante_email": rep_email,
                        "fecha_notificacion": str(fecha_noti), "autoriza_divulgacion": autoriza == "Sí",
                    }).execute()

                    st.success(f"✅ Reporte FOREIA001 guardado para **{nombre_generico}** (Inv: {num_inv_val}).")

                    if clasificacion in ["Evento adverso serio","Incidente adverso serio"]:
                        st.warning(
                            "⚠️ **EVENTO/INCIDENTE SERIO** — Según Resolución 4816/2008, "
                            "debe notificar al INVIMA dentro de las **72 horas** siguientes.\n\n"
                            "📧 tecnovigilancia@invima.gov.co | 📠 Fax: 4235656 ext. 104"
                        )
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error al guardar: {e}")

# ══════════════════════════════════════════
# CASOS REPORTADOS — Gestión Sección E
# ══════════════════════════════════════════
elif "Casos" in modulo:
    topbar("Casos Reportados", "Casos Reportados")

    try:
        tv_data = supabase.table("Tecnovigilancia").select("*").order("created_at", desc=True).execute().data
    except:
        tv_data = []

    if not tv_data:
        st.info("No hay casos reportados aún. Registra eventos en el módulo 🔍 Tecnovigilancia.")
    else:
        df_tv = pd.DataFrame(tv_data)

        # KPIs
        total   = len(df_tv)
        serios  = len(df_tv[df_tv["clasificacion"].str.contains("serio", case=False, na=False)]) if "clasificacion" in df_tv.columns else 0
        pendientes_e = len(df_tv[df_tv.get("causa_probable","").fillna("") == ""]) if "causa_probable" in df_tv.columns else 0

        st.markdown(f"""
        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-icon">📋</div>
            <div><div class="kpi-val">{total}</div><div class="kpi-label">Total casos reportados</div></div>
          </div>
          <div class="kpi-card" style="border-top-color:#e74c3c;">
            <div class="kpi-icon" style="background:rgba(231,76,60,.1);">🚨</div>
            <div><div class="kpi-val">{serios}</div><div class="kpi-label">Casos serios</div><div class="kpi-delta down">Requieren notif. INVIMA</div></div>
          </div>
          <div class="kpi-card" style="border-top-color:#27ae60;">
            <div class="kpi-icon" style="background:rgba(39,174,96,.1);">✅</div>
            <div><div class="kpi-val">{total - serios}</div><div class="kpi-label">Casos no serios</div></div>
          </div>
          <div class="kpi-card" style="border-top-color:#e67e22;">
            <div class="kpi-icon" style="background:rgba(230,126,34,.1);">⏳</div>
            <div><div class="kpi-val">{pendientes_e}</div><div class="kpi-label">Pendientes gestión E</div><div class="kpi-delta" style="color:#e67e22;">Sin causa registrada</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Lista de casos
        st.markdown('<div class="card"><div class="card-title">Seleccione un caso para gestionar la Sección E</div>', unsafe_allow_html=True)

        cols_lista = ["id","fecha_evento","numero_inventario","nombre_generico","clasificacion","reportante_nombre","causa_codigo"]
        cols_ok = [c for c in cols_lista if c in df_tv.columns]
        df_show = df_tv[cols_ok].copy()
        if "clasificacion" in df_show.columns:
            df_show["clasificacion"] = df_show["clasificacion"].fillna("")

        st.dataframe(df_show, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Selector de caso
        ids_disponibles = df_tv["id"].tolist()
        caso_opciones   = [f"Caso #{row['id']} — {row.get('nombre_generico','')} — {row.get('fecha_evento','')} — {row.get('clasificacion','')}"
                           for _, row in df_tv.iterrows()]

        caso_sel_label = st.selectbox("Seleccione el caso a gestionar:", ["— Seleccione un caso —"] + caso_opciones)

        if caso_sel_label != "— Seleccione un caso —":
            caso_id = int(caso_sel_label.split("#")[1].split(" ")[0])
            caso    = df_tv[df_tv["id"] == caso_id].iloc[0]

            # Info del caso
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### 📄 Resumen del caso")
            ci1,ci2,ci3 = st.columns(3)
            with ci1:
                st.markdown(f"**Dispositivo:** {caso.get('nombre_generico','')}")
                st.markdown(f"**N° Inventario:** {caso.get('numero_inventario','')}")
                st.markdown(f"**Fabricante:** {caso.get('fabricante','')}")
            with ci2:
                st.markdown(f"**Fecha evento:** {caso.get('fecha_evento','')}")
                st.markdown(f"**Clasificación:** {caso.get('clasificacion','')}")
                st.markdown(f"**Detección:** {caso.get('deteccion','')}")
            with ci3:
                st.markdown(f"**Reportante:** {caso.get('reportante_nombre','')}")
                st.markdown(f"**Profesión:** {caso.get('reportante_profesion','')}")
                st.markdown(f"**Área:** {caso.get('reportante_organizacion','')}")

            st.markdown("**Descripción del evento:**")
            st.info(caso.get("descripcion_evento","Sin descripción"))
            st.markdown("**Desenlace:**")
            desenlace_val = caso.get("desenlace","")
            if isinstance(desenlace_val, list):
                st.warning(", ".join(desenlace_val) if desenlace_val else "No especificado")
            else:
                st.warning(str(desenlace_val) if desenlace_val else "No especificado")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Formulario Sección E
            st.markdown('<div class="card">', unsafe_allow_html=True)
            seccion("📋 E. Gestión realizada — Diligenciar / Actualizar")

            with st.form(f"form_gestion_e_{caso_id}", clear_on_submit=False):
                ge1,ge2 = st.columns(2)
                with ge1:
                    causa_codigo_e = st.selectbox(
                        "E1. Causa probable (código NTC 5736:2009) *",
                        CAUSAS_NTC,
                        index=next((i for i,c in enumerate(CAUSAS_NTC) if c.startswith(str(caso.get("causa_codigo","")))), 0)
                    )
                    causa_desc_e = st.text_area("E1. Descripción de la causa probable *",
                        value=caso.get("causa_probable",""), height=100)
                    acciones_e = st.text_area("E2. Acciones correctivas y preventivas *",
                        value=caso.get("acciones_correctivas",""), height=100)

                with ge2:
                    rep_imp_e = st.radio("E3. ¿Reportó al importador/distribuidor?",
                        ["No","Sí"], horizontal=True,
                        index=1 if caso.get("reporto_importador") else 0)
                    fecha_rep_imp_e = None
                    if rep_imp_e == "Sí":
                        val_fecha_imp = date.today()
                        if caso.get("fecha_reporte_importador"):
                            try: val_fecha_imp = date.fromisoformat(str(caso["fecha_reporte_importador"])[:10])
                            except: pass
                        fecha_rep_imp_e = st.date_input("E3. Fecha de reporte al importador", value=val_fecha_imp)

                    disp_disp_e = st.radio("E4. ¿Dispositivo disponible para evaluación?",
                        ["Sí","No"], horizontal=True,
                        index=0 if caso.get("dispositivo_disponible") else 1)

                    disp_env_e = st.radio("E5. ¿Se ha enviado al distribuidor/importador?",
                        ["No","Sí"], horizontal=True,
                        index=1 if caso.get("dispositivo_enviado") else 0)
                    fecha_env_e = None
                    if disp_env_e == "Sí":
                        val_fecha_env = date.today()
                        if caso.get("fecha_envio_dispositivo"):
                            try: val_fecha_env = date.fromisoformat(str(caso["fecha_envio_dispositivo"])[:10])
                            except: pass
                        fecha_env_e = st.date_input("E5. Fecha de envío del dispositivo", value=val_fecha_env)

                if st.form_submit_button("💾 Guardar gestión Sección E", use_container_width=True):
                    if not causa_desc_e or not acciones_e:
                        st.error("❌ La causa probable y las acciones correctivas son obligatorias.")
                    else:
                        try:
                            supabase.table("Tecnovigilancia").update({
                                "causa_codigo":             causa_codigo_e.split(" — ")[0],
                                "causa_probable":           causa_desc_e,
                                "acciones_correctivas":     acciones_e,
                                "reporto_importador":       rep_imp_e == "Sí",
                                "fecha_reporte_importador": str(fecha_rep_imp_e) if fecha_rep_imp_e else None,
                                "dispositivo_disponible":   disp_disp_e == "Sí",
                                "dispositivo_enviado":      disp_env_e == "Sí",
                                "fecha_envio_dispositivo":  str(fecha_env_e) if fecha_env_e else None,
                            }).eq("id", caso_id).execute()
                            st.success(f"✅ Gestión del Caso #{caso_id} guardada correctamente.")
                            st.cache_data.clear()
                        except Exception as e:
                            st.error(f"❌ Error al actualizar: {e}")

            st.markdown('</div>', unsafe_allow_html=True)

        # Exportar
        st.markdown("<br>", unsafe_allow_html=True)
        csv = df_tv.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Exportar todos los casos a CSV", csv, "casos_tecnovigilancia.csv","text/csv")

# ══════════════════════════════════════════
# GESTIÓN DE RIESGOS
# ══════════════════════════════════════════
elif "Riesgos" in modulo:
    topbar("Gestión de Riesgos", "Gestión de Riesgos")
    ce, cc = st.columns([1,1.4])
    with ce:
        st.markdown('<div class="card"><div class="card-title">Evaluación de riesgo (AMEF)</div>', unsafe_allow_html=True)
        st.text_input("Equipo a evaluar")
        prob = st.slider("Probabilidad de falla", 1, 5, 3)
        imp  = st.slider("Impacto clínico",       1, 5, 3)
        det  = st.slider("Detectabilidad",        1, 5, 3)
        npr  = prob * imp * det
        col_npr   = "#27ae60" if npr<=20 else ("#e67e22" if npr<=60 else "#e74c3c")
        nivel_npr = "🟢 Bajo"  if npr<=20 else ("🟡 Medio" if npr<=60 else "🔴 Alto")
        st.markdown(f"""
        <div class="npr-box" style="background:{col_npr}18;border:1.5px solid {col_npr};">
            <div style="font-size:.76rem;color:#666;margin-bottom:4px;">NPR — Número de Prioridad de Riesgo</div>
            <div style="font-size:2.3rem;font-weight:700;color:{col_npr};">{npr}</div>
            <div style="font-size:1rem;font-weight:600;color:{col_npr};">{nivel_npr}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cc:
        st.markdown('<div class="card"><div class="card-title">Distribución de riesgo por servicio</div>', unsafe_allow_html=True)
        srvs = ["UCI","Urgencias","Hospitalización","Consulta ext."]
        fig_r = go.Figure()
        fig_r.add_bar(name="🔴 Alto",  x=srvs, y=[7,6,3,2],    marker_color="#e74c3c")
        fig_r.add_bar(name="🟡 Medio", x=srvs, y=[18,15,22,10], marker_color="#e67e22")
        fig_r.add_bar(name="🟢 Bajo",  x=srvs, y=[43,31,64,24], marker_color="#27ae60")
        lay_r = base_layout(270); lay_r.update(barmode="stack",
            legend=dict(orientation="h",y=1.05,x=1,xanchor="right",font_size=10),
            xaxis=dict(showgrid=False,tickfont_size=11), yaxis=dict(gridcolor="#f0f4f9"))
        fig_r.update_layout(lay_r); st.plotly_chart(fig_r, use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card"><div class="card-title">Equipos con riesgo alto — Seguimiento</div>', unsafe_allow_html=True)
    try:
        riesgo_data = supabase.table("Riesgos").select("*").order("npr", desc=True).execute().data
        if riesgo_data:
            df_r2 = pd.DataFrame(riesgo_data)
            cols = ["equipo","servicio","npr","nivel_riesgo","fecha_evaluacion","accion_requerida"]
            cols_ok = [c for c in cols if c in df_r2.columns]
            st.dataframe(df_r2[cols_ok], use_container_width=True, hide_index=True)
        else:
            st.info("No hay evaluaciones de riesgo registradas aún.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# MANTENIMIENTO
# ══════════════════════════════════════════
elif "Mantenimiento" in modulo:
    topbar("Mantenimiento Biomédico", "Mantenimiento")
    tab1, tab2, tab3 = st.tabs(["📅  Programar","📊  Indicadores","📋  Historial"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("form_mant", clear_on_submit=True):
            c1,c2,c3 = st.columns(3)
            with c1:
                eq_m    = st.text_input("Equipo biomédico *")
                tipo_m  = st.selectbox("Tipo",["Preventivo","Correctivo","Calibración","Verificación metrológica"])
                fecha_m = st.date_input("Fecha programada", value=date.today())
            with c2:
                tecnico_m   = st.text_input("Técnico responsable")
                prioridad_m = st.selectbox("Prioridad",["🔴 Alta","🟡 Media","🟢 Baja"])
                costo_m     = st.number_input("Costo estimado (COP)", min_value=0, step=10000)
            with c3:
                servicio_m = st.selectbox("Servicio",["UCI","Urgencias","Hospitalización","Consulta externa"])
                duracion_m = st.number_input("Duración estimada (h)", min_value=0.5, max_value=48.0, step=0.5, value=2.0)
                repuestos  = st.text_input("Repuestos requeridos")
            actividades_m = st.text_area("Actividades a realizar", height=80)
            if st.form_submit_button("📅 Programar mantenimiento"):
                if eq_m:
                    try:
                        supabase.table("Mantenimiento").insert({
                            "equipo": eq_m, "tipo_mantenimiento": tipo_m,
                            "fecha_programada": str(fecha_m), "tecnico": tecnico_m,
                            "prioridad": prioridad_m, "costo": float(costo_m),
                            "servicio": servicio_m, "duracion_horas": float(duracion_m),
                            "repuestos": repuestos, "actividades": actividades_m,
                            "estado": "Programado"
                        }).execute()
                        st.success(f"✅ **{tipo_m}** programado para **{eq_m}** el {fecha_m.strftime('%d/%m/%Y')}.")
                    except Exception as e:
                        st.error(f"❌ Error al guardar: {e}")
                else:
                    st.error("Ingrese el nombre del equipo.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        ci1,ci2,ci3 = st.columns(3)
        with ci1:
            st.markdown('<div class="card"><div class="card-title">Cumplimiento preventivo</div>', unsafe_allow_html=True)
            fig_g = go.Figure(go.Indicator(mode="gauge+number", value=87,
                number={"suffix":"%","font":{"size":30}},
                gauge=dict(axis=dict(range=[0,100]), bar=dict(color="#1a8fd1"),
                    steps=[dict(range=[0,60],color="#fde8e8"),dict(range=[60,80],color="#fef9e7"),dict(range=[80,100],color="#eafaf1")])))
            fig_g.update_layout(height=195, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="white")
            st.plotly_chart(fig_g, use_container_width=True, config=PLOT_CFG)
            st.markdown('</div>', unsafe_allow_html=True)
        with ci2:
            st.markdown('<div class="card"><div class="card-title">MTBF por servicio (días)</div>', unsafe_allow_html=True)
            fig_mtbf = go.Figure(go.Bar(x=["UCI","Urgencias","Hosp.","Consulta"], y=[180,120,210,260],
                marker_color="#0D2B52", text=[180,120,210,260], textposition="outside"))
            lay_m = base_layout(195); lay_m.update(xaxis=dict(showgrid=False,tickfont_size=10), yaxis=dict(gridcolor="#f0f4f9",visible=False))
            fig_mtbf.update_layout(lay_m); st.plotly_chart(fig_mtbf, use_container_width=True, config=PLOT_CFG)
            st.markdown('</div>', unsafe_allow_html=True)
        with ci3:
            st.markdown('<div class="card"><div class="card-title">Distribución por tipo</div>', unsafe_allow_html=True)
            fig_tipo = go.Figure(go.Pie(labels=["Preventivo","Correctivo","Calibración","Verificación"],
                values=[55,25,12,8], hole=0.48, marker_colors=["#1a8fd1","#e74c3c","#27ae60","#e67e22"]))
            fig_tipo.update_layout(height=195, margin=dict(l=0,r=0,t=4,b=0), paper_bgcolor="white",
                showlegend=True, legend=dict(orientation="h",y=-0.3,font_size=9))
            st.plotly_chart(fig_tipo, use_container_width=True, config=PLOT_CFG)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card"><div class="card-title">Historial de mantenimientos</div>', unsafe_allow_html=True)
        try:
            mant_data = supabase.table("Mantenimiento").select("*").order("created_at", desc=True).execute().data
            if mant_data:
                df_mant = pd.DataFrame(mant_data)
                cols = ["equipo","tipo_mantenimiento","fecha_programada","tecnico","costo","estado"]
                cols_ok = [c for c in cols if c in df_mant.columns]
                st.dataframe(df_mant[cols_ok], use_container_width=True, hide_index=True)
            else:
                st.info("No hay mantenimientos registrados aún.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
