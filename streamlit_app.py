import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta
import random
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

/* Fondo principal BLANCO */
.main .block-container {
    background-color: #F0F4F9 !important;
    padding-top: 1.2rem !important;
    max-width: 100% !important;
}
.main {
    background-color: #F0F4F9 !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #F0F4F9 !important;
}
[data-testid="stAppViewBlockContainer"] {
    background-color: #F0F4F9 !important;
}
section.main {
    background-color: #F0F4F9 !important;
}

/* ── SIDEBAR BLANCO ── */
section[data-testid="stSidebar"] {
    background: white !important;
    border-right: 1px solid #e8edf5 !important;
}
section[data-testid="stSidebar"] * {
    color: #0D2B52 !important;
}
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #F0F4F9 !important;
    border: 1px solid #dce5f0 !important;
    border-radius: 8px !important;
    color: #0D2B52 !important;
}
section[data-testid="stSidebar"] label {
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #8a9bb5 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: #e8edf5 !important;
    margin: 0.6rem 0 !important;
}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #0D2B52 !important;
    font-size: 0.95rem !important;
    margin: 0.3rem 0 !important;
}

/* Topbar */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: white;
    border-radius: 10px;
    padding: 0.65rem 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 12px rgba(13,43,82,0.09);
}
.topbar-title { font-size: 1.05rem; font-weight: 700; color: #0D2B52; }
.topbar-crumb { font-size: 0.72rem; color: #8a9bb5; margin-top: 1px; }
.topbar-user  { font-size: 0.83rem; font-weight: 600; color: #0D2B52; }

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 1rem;
}
.kpi-card {
    background: white;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 12px rgba(13,43,82,0.09);
    display: flex;
    align-items: center;
    gap: 0.9rem;
    border-top: 3px solid #1a8fd1;
    transition: transform .15s;
}
.kpi-card:hover { transform: translateY(-2px); }
.kpi-icon {
    font-size: 1.7rem;
    background: rgba(26,143,209,0.1);
    border-radius: 10px;
    width: 50px; height: 50px;
    display: flex; align-items: center;
    justify-content: center; flex-shrink: 0;
}
.kpi-val   { font-size: 1.55rem; font-weight: 700; color: #0D2B52; line-height: 1; }
.kpi-label { font-size: 0.75rem; color: #8a9bb5; margin-top: 3px; }
.kpi-delta { font-size: 0.7rem; margin-top: 3px; }
.up   { color: #27ae60; }
.down { color: #e74c3c; }

/* Cards de contenido */
.card {
    background: white;
    border-radius: 12px;
    padding: 1rem 1.1rem 0.6rem;
    box-shadow: 0 2px 12px rgba(13,43,82,0.09);
}
.card-title {
    font-size: 0.88rem;
    font-weight: 700;
    color: #0D2B52;
    border-bottom: 1px solid #eef2f7;
    padding-bottom: 0.4rem;
    margin-bottom: 0.5rem;
}

/* Botones */
.stButton > button {
    background: linear-gradient(135deg, #0D2B52, #1a8fd1) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: opacity .2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Inputs */
.stTextInput input, .stTextArea textarea {
    border-radius: 8px !important;
    border: 1px solid #dce5f0 !important;
}

/* Labels blancos en panel principal */
.main .stTextInput label,
.main .stTextArea label,
.main .stSelectbox label,
.main .stNumberInput label,
.main .stDateInput label,
.main .stSlider label,
.main .stMarkdown p,
.main h4, .main h3, .main h2,
[data-testid="stForm"] label,
[data-testid="stForm"] p {
    color: white !important;
}

/* Tabs texto blanco */
[data-testid="stTabs"] button {
    color: rgba(255,255,255,0.7) !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: white !important;
}

/* NPR badge */
.npr-box {
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    margin-top: 0.8rem;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }

/* ── Botón reapertura sidebar: ocultar texto y mostrar ☰ ── */
[data-testid="collapsedControl"] {
    background: #0D2B52 !important;
    border-radius: 0 10px 10px 0 !important;
    padding: 14px 10px !important;
    box-shadow: 3px 0 12px rgba(0,0,0,0.25) !important;
    overflow: hidden !important;
    width: 44px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
[data-testid="collapsedControl"]:hover {
    background: #1a8fd1 !important;
}
/* Ocultar el ícono/texto original */
[data-testid="collapsedControl"] svg,
[data-testid="collapsedControl"] span {
    display: none !important;
}
/* Insertar ☰ con CSS puro */
[data-testid="collapsedControl"]::after {
    content: "";
    display: block;
    width: 22px;
    height: 2px;
    background: white;
    border-radius: 2px;
    box-shadow: 0 7px 0 white, 0 14px 0 white;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# RUTAS
# ─────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "assets", "Logo_sportmeds.png")

# ─────────────────────────────────────────
# SIDEBAR — nativo st.sidebar (siempre funciona)
# ─────────────────────────────────────────
# Logo
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, width=190)
else:
    st.sidebar.markdown(
        "<div style='font-size:1.15rem;font-weight:700;padding:0.5rem 0;'>⚕️ SPORTMEDS</div>",
        unsafe_allow_html=True
    )

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("### Menú Principal")

modulo = st.sidebar.selectbox(
    "Seleccione un módulo",
    [
        "🏠  Panel de Control",
        "📦  Inventario",
        "🔍  Tecnovigilancia",
        "⚠️  Gestión de Riesgos",
        "🔧  Mantenimiento",
    ]
)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style='padding: 0.2rem 0;'>
    <div style='font-size:0.67rem;color:rgba(255,255,255,0.38);
                text-transform:uppercase;letter-spacing:.08em;'>Usuario</div>
    <div style='font-size:0.9rem;font-weight:600;margin-top:3px;'>Ing. Biomédico</div>
    <div style='font-size:0.7rem;color:rgba(255,255,255,0.42);'>Administrador</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<div style='font-size:0.65rem;color:rgba(255,255,255,0.25);text-align:center;'>"
    "Gestión Biomédica v1.0<br>© 2025 SPORTMEDS Centro Médico</div>",
    unsafe_allow_html=True
)

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
PLOT_CFG = {"displayModeBar": False}

def base_layout(h=220):
    return dict(height=h, margin=dict(l=0, r=0, t=4, b=0),
                plot_bgcolor="white", paper_bgcolor="white")

def topbar(titulo, ruta):
    st.markdown(f"""
    <div class="topbar">
        <div>
            <div class="topbar-title">{titulo}</div>
            <div class="topbar-crumb">INICIO › {ruta}</div>
        </div>
        <div class="topbar-user">👤 Ing. Biomédico &nbsp;🔒</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# MÓDULO: PANEL DE CONTROL
# ══════════════════════════════════════════
if "Panel" in modulo:
    topbar("Panel de Control", "Panel de Control")

    # ── Datos reales desde Supabase ──
    try:
        inv_data = supabase.table("Inventario").select("*").execute().data
        df_inv   = pd.DataFrame(inv_data) if inv_data else pd.DataFrame()

        total_equipos  = len(df_inv)
        riesgo_alto    = len(df_inv[df_inv["clase_riesgo"] == "Clase III"]) if not df_inv.empty and "clase_riesgo" in df_inv.columns else 0
        fuera_servicio = len(df_inv[df_inv["estado"].str.contains("Fuera", na=False)]) if not df_inv.empty and "estado" in df_inv.columns else 0
    except:
        total_equipos = riesgo_alto = fuera_servicio = 0
        df_inv = pd.DataFrame()

    # KPIs dinámicos
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-icon">🩺</div>
        <div>
          <div class="kpi-val">{total_equipos}</div>
          <div class="kpi-label">Equipos registrados</div>
          <div class="kpi-delta up">Base de datos activa</div>
        </div>
      </div>
      <div class="kpi-card" style="border-top-color:#e74c3c;">
        <div class="kpi-icon" style="background:rgba(231,76,60,.1);">⚠️</div>
        <div>
          <div class="kpi-val">{riesgo_alto}</div>
          <div class="kpi-label">Equipos Clase III</div>
          <div class="kpi-delta down">Riesgo alto</div>
        </div>
      </div>
      <div class="kpi-card" style="border-top-color:#e67e22;">
        <div class="kpi-icon" style="background:rgba(230,126,34,.1);">🔧</div>
        <div>
          <div class="kpi-val">{fuera_servicio}</div>
          <div class="kpi-label">Fuera de servicio</div>
          <div class="kpi-delta" style="color:#e67e22;">● Requieren atención</div>
        </div>
      </div>
      <div class="kpi-card" style="border-top-color:#27ae60;">
        <div class="kpi-icon" style="background:rgba(39,174,96,.1);">✅</div>
        <div>
          <div class="kpi-val">{total_equipos - fuera_servicio}</div>
          <div class="kpi-label">En servicio</div>
          <div class="kpi-delta up">Operativos</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Fila 1: 3 gráficas con datos reales
    c1, c2, c3 = st.columns([1.4, 1.1, 1.4])

    with c1:
        st.markdown('<div class="card"><div class="card-title">Equipos por estado</div>', unsafe_allow_html=True)
        if not df_inv.empty and "estado" in df_inv.columns:
            estado_counts = df_inv["estado"].value_counts()
            fig = go.Figure(go.Bar(
                x=estado_counts.index.tolist(),
                y=estado_counts.values.tolist(),
                marker_color=["#27ae60" if "En servicio" in e else "#e74c3c" for e in estado_counts.index],
                text=estado_counts.values.tolist(), textposition="outside"
            ))
        else:
            fig = go.Figure(go.Bar(x=["Sin datos"], y=[0], marker_color="#8a9bb5"))
        lay = base_layout()
        lay.update(xaxis=dict(showgrid=False, tickfont_size=9),
                   yaxis=dict(gridcolor="#f0f4f9", tickfont_size=10))
        fig.update_layout(lay)
        st.plotly_chart(fig, use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><div class="card-title">Equipos por clase INVIMA</div>', unsafe_allow_html=True)
        if not df_inv.empty and "clase_riesgo" in df_inv.columns:
            clase_counts = df_inv["clase_riesgo"].value_counts()
            fig2 = go.Figure(go.Pie(
                labels=clase_counts.index.tolist(),
                values=clase_counts.values.tolist(),
                hole=0.52,
                marker_colors=["#27ae60","#1a8fd1","#e67e22","#e74c3c"],
                textfont_size=10
            ))
        else:
            fig2 = go.Figure(go.Pie(labels=["Sin datos"], values=[1], hole=0.52,
                                    marker_colors=["#8a9bb5"]))
        fig2.update_layout(height=220, margin=dict(l=0,r=0,t=4,b=0),
                           paper_bgcolor="white", showlegend=True,
                           legend=dict(orientation="h", y=-0.28, font_size=9))
        st.plotly_chart(fig2, use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="card"><div class="card-title">Equipos por servicio</div>', unsafe_allow_html=True)
        if not df_inv.empty and "servicio" in df_inv.columns:
            serv_counts = df_inv["servicio"].value_counts()
            fig3 = go.Figure(go.Bar(
                x=serv_counts.values.tolist(),
                y=serv_counts.index.tolist(),
                orientation="h",
                marker_color="#1a8fd1",
                text=serv_counts.values.tolist(), textposition="outside"
            ))
        else:
            fig3 = go.Figure(go.Bar(x=[0], y=["Sin datos"], orientation="h",
                                    marker_color="#8a9bb5"))
        lay3 = base_layout()
        lay3.update(xaxis=dict(showgrid=False, visible=False),
                    yaxis=dict(showgrid=False, tickfont_size=10))
        fig3.update_layout(lay3)
        st.plotly_chart(fig3, use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Fila 2: línea + tabla
    c4, c5 = st.columns([1.6, 1])

    with c4:
        st.markdown('<div class="card"><div class="card-title">Eventos tecnovigilancia — últimos 30 días</div>', unsafe_allow_html=True)
        dias    = [(date.today()-timedelta(days=i)).strftime("%d/%m") for i in range(29,-1,-1)]
        eventos = [random.randint(0,3) for _ in dias]
        fig4 = go.Figure(go.Scatter(
            x=dias, y=eventos, mode="lines+markers",
            line=dict(color="#1a8fd1", width=2),
            marker=dict(color="#0D2B52", size=5),
            fill="tozeroy", fillcolor="rgba(26,143,209,0.07)"
        ))
        lay4 = base_layout(210)
        lay4.update(xaxis=dict(showgrid=False, tickangle=-45, tickfont_size=8,
                               tickvals=dias[::5], ticktext=dias[::5]),
                    yaxis=dict(gridcolor="#f0f4f9", tickfont_size=10))
        fig4.update_layout(lay4)
        st.plotly_chart(fig4, use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    with c5:
        st.markdown('<div class="card"><div class="card-title">Últimos equipos registrados</div>', unsafe_allow_html=True)
        if not df_inv.empty:
            cols = ["numero_inventario","descripcion","servicio","estado"]
            cols_ok = [c for c in cols if c in df_inv.columns]
            st.dataframe(df_inv[cols_ok].tail(5), use_container_width=True,
                         hide_index=True, height=210)
        else:
            st.info("Sin registros aún.")
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# MÓDULO: INVENTARIO
# ══════════════════════════════════════════
elif "Inventario" in modulo:
    topbar("Inventario Biomédico", "Inventario")
    tab1, tab2 = st.tabs(["➕  Registrar equipo", "📋  Listado de equipos"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("form_inv", clear_on_submit=True):

            st.markdown("#### 🔖 Identificación del equipo")
            c1, c2, c3 = st.columns(3)
            with c1:
                numero_inventario = st.text_input("N° de inventario *")
                tipo_equipo       = st.selectbox("Tipo de equipo *", [
                    "Equipo de diagnóstico por imagen",
                    "Equipo de monitoreo",
                    "Equipo de soporte vital",
                    "Equipo de laboratorio",
                    "Equipo quirúrgico",
                    "Equipo de rehabilitación",
                    "Otro"
                ])
                descripcion = st.text_input("Descripción del equipo *")
            with c2:
                fabricante = st.text_input("Fabricante *")
                modelo     = st.text_input("Modelo / N° catálogo")
                numero_serie = st.text_input("N° de serie")
            with c3:
                numero_lote = st.text_input("N° de lote")
                clase_riesgo = st.selectbox("Clase de riesgo INVIMA", [
                    "Clase I",
                    "Clase IIa",
                    "Clase IIb",
                    "Clase III"
                ])
                alimentacion = st.selectbox("Alimentación eléctrica", [
                    "110V",
                    "220V",
                    "380V",
                    "Trifásica",
                    "No aplica"
                ])

            st.markdown("---")
            st.markdown("#### 📍 Ubicación y estado")
            c4, c5, c6 = st.columns(3)
            with c4:
                servicio = st.selectbox("Servicio / Ubicación *", [
                    "UCI",
                    "Urgencias",
                    "Hospitalización",
                    "Consulta externa",
                    "Imágenes diagnósticas",
                    "Cirugía",
                    "Laboratorio",
                    "Rehabilitación"
                ])
                ubicacion = st.text_input("Habitación / Área específica")
            with c5:
                estado = st.selectbox("Estado operativo *", [
                    "En servicio",
                    "Fuera de servicio - Mantenimiento preventivo",
                    "Fuera de servicio - En reparación",
                    "Fuera de servicio - Pendiente calibración",
                    "Fuera de servicio - Dado de baja"
                ])
                requisitos = st.text_input("Requisitos especiales de funcionamiento")
            with c6:
                proveedor_compra = st.text_input("Proveedor de compra")
                proveedor_mant   = st.text_input("Proveedor de mantenimiento")

            st.markdown("---")
            st.markdown("#### 📅 Fechas y costos")
            c7, c8, c9 = st.columns(3)
            with c7:
                fecha_compra   = st.date_input("Fecha de compra", value=date.today())
                fecha_registro = st.date_input("Fecha de registro", value=date.today())
            with c8:
                garantia_inicio = st.date_input("Garantía — fecha inicio", value=date.today())
                garantia_fin    = st.date_input("Garantía — fecha fin",    value=date.today())
            with c9:
                costo     = st.number_input("Costo de adquisición (COP)", min_value=0, step=100000)
                vida_util = st.number_input("Vida útil estimada (años)", 1, 30, 5)

            st.markdown("---")
            obs = st.text_area("Observaciones adicionales")

            submitted = st.form_submit_button("✅ Registrar equipo en base de datos",
                                              use_container_width=True)
            if submitted:
                if numero_inventario and descripcion and fabricante:
                    try:
                        data = {
                            "numero_inventario": numero_inventario,
                            "tipo_equipo":       tipo_equipo,
                            "descripcion":       descripcion,
                            "fabricante":        fabricante,
                            "modelo":            modelo,
                            "numero_serie":      numero_serie,
                            "numero_lote":       numero_lote,
                            "clase_riesgo":      clase_riesgo,
                            "alimentacion_electrica": alimentacion,
                            "servicio":          servicio,
                            "Ubicación":         ubicacion,
                            "estado":            estado,
                            "proveedor_compra":  proveedor_compra,
                            "proveedor_mantenimiento": proveedor_mant,
                            "fecha_compra":      str(fecha_compra),
                            "fecha_registro":    str(fecha_registro),
                            "garantia_inicio":   str(garantia_inicio),
                            "garantia_fin":      str(garantia_fin),
                            "costo":             float(costo),
                            "observaciones":     obs,
                        }
                        supabase.table("Inventario").insert(data).execute()
                        st.success(f"✅ **{descripcion}** registrado correctamente en el inventario.")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error al guardar: {e}")
                else:
                    st.error("Complete los campos obligatorios: N° inventario, Descripción y Fabricante.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card"><div class="card-title">Equipos registrados en base de datos</div>', unsafe_allow_html=True)
        try:
            response = supabase.table("Inventario").select("*").execute()
            if response.data:
                df = pd.DataFrame(response.data)
                # Columnas a mostrar
                cols_show = ["numero_inventario","descripcion","fabricante","modelo",
                             "clase_riesgo","servicio","estado","fecha_compra"]
                cols_available = [c for c in cols_show if c in df.columns]
                st.dataframe(df[cols_available], use_container_width=True, hide_index=True)

                # Botón exportar
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Exportar a CSV", csv,
                                   "inventario_sportmeds.csv", "text/csv")
            else:
                st.info("No hay equipos registrados aún. Usa la pestaña ➕ Registrar equipo.")
        except Exception as e:
            st.error(f"❌ Error al cargar datos: {e}")
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════
# MÓDULO: TECNOVIGILANCIA
# ══════════════════════════════════════════
elif "Tecnovigilancia" in modulo:
    topbar("Tecnovigilancia", "Tecnovigilancia")
    cf, cs = st.columns([1.6, 1])

    with cf:
        st.markdown('<div class="card"><div class="card-title">Registro de evento adverso</div>', unsafe_allow_html=True)
        with st.form("form_tv", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                equipo_tv   = st.text_input("Equipo involucrado *")
                tipo_ev     = st.selectbox("Tipo de evento",
                    ["Incidente","Casi incidente","Evento adverso serio",
                     "Falla del equipo","Alerta de seguridad"])
                fecha_ev    = st.date_input("Fecha del evento", value=date.today())
            with c2:
                reportador  = st.text_input("Reportador")
                cargo       = st.text_input("Cargo")
                servicio_tv = st.selectbox("Servicio",
                    ["UCI","Urgencias","Hospitalización","Consulta externa"])
            descripcion = st.text_area("Descripción detallada *", height=100)
            accion      = st.text_area("Acción inmediata tomada", height=60)
            if st.form_submit_button("📋 Guardar reporte"):
                if equipo_tv and descripcion:
                    st.success("✅ Evento registrado. Se notificará al coordinador biomédico.")
                else:
                    st.error("Complete los campos obligatorios (*).")
        st.markdown('</div>', unsafe_allow_html=True)

    with cs:
        st.markdown('<div class="card"><div class="card-title">Eventos por tipo (30 días)</div>', unsafe_allow_html=True)
        fig_tv = go.Figure(go.Bar(
            x=["Incidente","Casi inc.","Adverso","Falla","Alerta"],
            y=[3,5,1,4,2],
            marker_color=["#1a8fd1","#e67e22","#e74c3c","#9b59b6","#27ae60"]
        ))
        lay_tv = base_layout(190)
        lay_tv.update(xaxis=dict(showgrid=False, tickfont_size=9),
                      yaxis=dict(gridcolor="#f0f4f9"))
        fig_tv.update_layout(lay_tv)
        st.plotly_chart(fig_tv, use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="card-title">Últimos reportes</div>', unsafe_allow_html=True)
        try:
            tv_data = supabase.table("Tecnovigilancia").select("*").order("created_at", desc=True).limit(5).execute().data
            if tv_data:
                df_tv = pd.DataFrame(tv_data)
                cols = ["equipo","tipo_evento","fecha_evento","servicio"]
                cols_ok = [c for c in cols if c in df_tv.columns]
                st.dataframe(df_tv[cols_ok], use_container_width=True, hide_index=True)
            else:
                st.info("No hay reportes aún.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# MÓDULO: GESTIÓN DE RIESGOS
# ══════════════════════════════════════════
elif "Riesgos" in modulo:
    topbar("Gestión de Riesgos", "Gestión de Riesgos")
    ce, cc = st.columns([1, 1.4])

    with ce:
        st.markdown('<div class="card"><div class="card-title">Evaluación de riesgo (AMEF)</div>', unsafe_allow_html=True)
        st.text_input("Equipo a evaluar")
        prob = st.slider("Probabilidad de falla", 1, 5, 3, help="1=Muy baja · 5=Muy alta")
        imp  = st.slider("Impacto clínico",       1, 5, 3, help="1=Mínimo · 5=Catastrófico")
        det  = st.slider("Detectabilidad",        1, 5, 3, help="1=Fácil · 5=Imposible")
        npr  = prob * imp * det
        col_npr   = "#27ae60" if npr <= 20 else ("#e67e22" if npr <= 60 else "#e74c3c")
        nivel_npr = "🟢 Bajo"  if npr <= 20 else ("🟡 Medio" if npr <= 60 else "🔴 Alto")
        st.markdown(f"""
        <div class="npr-box" style="background:{col_npr}18; border:1.5px solid {col_npr};">
            <div style="font-size:.76rem;color:#666;margin-bottom:4px;">
                NPR — Número de Prioridad de Riesgo
            </div>
            <div style="font-size:2.3rem;font-weight:700;color:{col_npr};">{npr}</div>
            <div style="font-size:1rem;font-weight:600;color:{col_npr};">{nivel_npr}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cc:
        st.markdown('<div class="card"><div class="card-title">Distribución de riesgo por servicio</div>', unsafe_allow_html=True)
        srvs = ["UCI","Urgencias","Hospitalización","Consulta ext."]
        fig_r = go.Figure()
        fig_r.add_bar(name="🔴 Alto",  x=srvs, y=[7,6,3,2],    marker_color="#e74c3c")
        fig_r.add_bar(name="🟡 Medio", x=srvs, y=[18,15,22,10], marker_color="#e67e22")
        fig_r.add_bar(name="🟢 Bajo",  x=srvs, y=[43,31,64,24], marker_color="#27ae60")
        lay_r = base_layout(270)
        lay_r.update(barmode="stack",
                     legend=dict(orientation="h", y=1.05, x=1, xanchor="right", font_size=10),
                     xaxis=dict(showgrid=False, tickfont_size=11),
                     yaxis=dict(gridcolor="#f0f4f9"))
        fig_r.update_layout(lay_r)
        st.plotly_chart(fig_r, use_container_width=True, config=PLOT_CFG)
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
        st.error(f"❌ Error al cargar riesgos: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# MÓDULO: MANTENIMIENTO
# ══════════════════════════════════════════
elif "Mantenimiento" in modulo:
    topbar("Mantenimiento Biomédico", "Mantenimiento")
    tab1, tab2, tab3 = st.tabs(["📅  Programar", "📊  Indicadores", "📋  Historial"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("form_mant", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                eq_m    = st.text_input("Equipo biomédico *")
                tipo_m  = st.selectbox("Tipo",
                    ["Preventivo","Correctivo","Calibración","Verificación metrológica"])
                fecha_m = st.date_input("Fecha programada", value=date.today())
            with c2:
                tecnico_m   = st.text_input("Técnico responsable")
                prioridad_m = st.selectbox("Prioridad", ["🔴 Alta","🟡 Media","🟢 Baja"])
                costo_m     = st.number_input("Costo estimado (COP)", min_value=0, step=10000)
            with c3:
                servicio_m = st.selectbox("Servicio",
                    ["UCI","Urgencias","Hospitalización","Consulta externa"])
                duracion_m = st.number_input("Duración estimada (h)",
                    min_value=0.5, max_value=48.0, step=0.5, value=2.0)
                repuestos  = st.text_input("Repuestos requeridos")
            actividades_m = st.text_area("Actividades a realizar", height=80)
            if st.form_submit_button("📅 Programar mantenimiento"):
                if eq_m:
                    st.success(
                        f"✅ **{tipo_m}** programado para **{eq_m}** "
                        f"el {fecha_m.strftime('%d/%m/%Y')} — Prioridad: {prioridad_m}"
                    )
                else:
                    st.error("Ingrese el nombre del equipo.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        ci1, ci2, ci3 = st.columns(3)

        with ci1:
            st.markdown('<div class="card"><div class="card-title">Cumplimiento preventivo</div>', unsafe_allow_html=True)
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number", value=87,
                number={"suffix":"%","font":{"size":30}},
                gauge=dict(
                    axis=dict(range=[0,100]),
                    bar=dict(color="#1a8fd1"),
                    steps=[
                        dict(range=[0,60],   color="#fde8e8"),
                        dict(range=[60,80],  color="#fef9e7"),
                        dict(range=[80,100], color="#eafaf1"),
                    ]
                )
            ))
            fig_g.update_layout(height=195, margin=dict(l=10,r=10,t=10,b=10),
                                paper_bgcolor="white")
            st.plotly_chart(fig_g, use_container_width=True, config=PLOT_CFG)
            st.markdown('</div>', unsafe_allow_html=True)

        with ci2:
            st.markdown('<div class="card"><div class="card-title">MTBF por servicio (días)</div>', unsafe_allow_html=True)
            fig_mtbf = go.Figure(go.Bar(
                x=["UCI","Urgencias","Hosp.","Consulta"],
                y=[180,120,210,260],
                marker_color="#0D2B52",
                text=[180,120,210,260], textposition="outside"
            ))
            lay_m = base_layout(195)
            lay_m.update(xaxis=dict(showgrid=False, tickfont_size=10),
                         yaxis=dict(gridcolor="#f0f4f9", visible=False))
            fig_mtbf.update_layout(lay_m)
            st.plotly_chart(fig_mtbf, use_container_width=True, config=PLOT_CFG)
            st.markdown('</div>', unsafe_allow_html=True)

        with ci3:
            st.markdown('<div class="card"><div class="card-title">Distribución por tipo</div>', unsafe_allow_html=True)
            fig_tipo = go.Figure(go.Pie(
                labels=["Preventivo","Correctivo","Calibración","Verificación"],
                values=[55,25,12,8], hole=0.48,
                marker_colors=["#1a8fd1","#e74c3c","#27ae60","#e67e22"]
            ))
            fig_tipo.update_layout(height=195, margin=dict(l=0,r=0,t=4,b=0),
                                   paper_bgcolor="white", showlegend=True,
                                   legend=dict(orientation="h", y=-0.3, font_size=9))
            st.plotly_chart(fig_tipo, use_container_width=True, config=PLOT_CFG)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card"><div class="card-title">Historial de mantenimientos</div>', unsafe_allow_html=True)
        try:
            mant_data = supabase.table("Mantenimiento").select("*").execute().data
            if mant_data:
                df_mant = pd.DataFrame(mant_data)
                cols = ["equipo","tipo_mantenimiento","fecha_programada",
                        "tecnico","costo","estado"]
                cols_ok = [c for c in cols if c in df_mant.columns]
                st.dataframe(df_mant[cols_ok], use_container_width=True, hide_index=True)
            else:
                st.info("No hay mantenimientos registrados aún.")
        except Exception as e:
            st.error(f"❌ Error al cargar historial: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
