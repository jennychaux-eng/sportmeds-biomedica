from config.config import (
    supabase,
    LOGO_PATH,
    BASE_DIR,
    get_fecha_local,
    get_base64_image
)
import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go
import base64
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from supabase import create_client, Client
from inventario.view import render as inventario_view
from tecnovigilancia.view import render as tecnovigilancia_view
from config.constants import CAUSAS_NTC
from casos.view import render as casos_view

# ==========================================
# AUTENTICACIÓN
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_role" not in st.session_state:
    st.session_state.user_role = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "user_profesion" not in st.session_state:
    st.session_state.user_profesion = ""

if "user_telefono" not in st.session_state:
    st.session_state.user_telefono = ""

if "user_area" not in st.session_state:
    st.session_state.user_area = ""

if "user_gender" not in st.session_state:
    st.session_state.user_gender = ""

from auth.login import login_page

# ─────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Gestión Biomédica SPORTMEDS",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ==========================================
# BLOQUEO DE ACCESO
# ==========================================

if not st.session_state.logged_in:

    st.markdown("""
    <style>
    section[data-testid="stSidebar"]{
        display:none;
    }
    </style>
    """, unsafe_allow_html=True)

    login_page()
    st.stop()
    
# ─────────────────────────────────────────
# ESTILOS
# ─────────────────────────────────────────
from config.theme import load_theme
load_theme()

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, width=190)
else:
    st.sidebar.markdown(
        "<div style='font-size:1.15rem;font-weight:700;padding:0.5rem 0;'>⚕️ SPORTMEDS</div>",
        unsafe_allow_html=True
    )

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("### Menú Principal")

ROL_MENUS = {

    "Gerente": [
        "🏠  Panel de Control",
        "📦  Inventario",
        "🔍  Tecnovigilancia",
        "📋  Casos reportados",
        "⚠️  Gestión de Riesgos",
        "🔧  Mantenimiento",
    ],

    "Ingeniero biomédico/a": [
        "🏠  Panel de Control",
        "📦  Inventario",
        "🔍  Tecnovigilancia",
        "📋  Casos reportados",
        "⚠️  Gestión de Riesgos",
        "🔧  Mantenimiento",
    ],

    "Cirujano/a": [
        "🏠  Panel de Control",
        "🔍  Tecnovigilancia",
    ],

    "Médico/a": [
        "🏠  Panel de Control",
        "🔍  Tecnovigilancia",
    ],

    "Enfermero/a": [
        "🏠  Panel de Control",
        "🔍  Tecnovigilancia",
    ],

    "Instrumentador quirurgico/a": [
        "🏠  Panel de Control",
        "🔍  Tecnovigilancia",
    ],

    "Encargado del mantenimiento": [
        "🔧  Mantenimiento",
    ],

    "Técnico Biomédico": [
        "🏠  Panel de Control",
        "🔧  Mantenimiento",
    ],

}

def normalize_role(role: str) -> str:
    if not role:
        return ""
    role_key = role.strip().lower()
    normalized = {
        "ingeniero biomédico": "Ingeniero biomédico/a",
        "ingeniero biomedico": "Ingeniero biomédico/a",
        "ingeniero biomédico/a": "Ingeniero biomédico/a",
        "cirujano/a": "Cirujano/a",
        "médico/a": "Médico/a",
        "medico/a": "Médico/a",
        "enfermero/a": "Enfermero/a",
        "instrumentador quirurgico/a": "Instrumentador quirurgico/a",
        "encargado del mantenimiento": "Encargado del mantenimiento",
        "técnico biomédico": "Técnico Biomédico",
        "tecnico biomedico": "Técnico Biomédico",
        "administrador": "Administrador",
        "consulta": "Consulta",
    }
    return normalized.get(role_key, role)

menu_usuario = ROL_MENUS.get(
    normalize_role(st.session_state.user_role),
    ["🏠  Panel de Control"]
)

if "sidebar_modulo" not in st.session_state:
    st.session_state.sidebar_modulo = menu_usuario[0] if menu_usuario else "🏠  Panel de Control"

if "go_to_module" in st.session_state and st.session_state.go_to_module in menu_usuario:
    st.session_state.sidebar_modulo = st.session_state.go_to_module
    del st.session_state.go_to_module

if st.session_state.sidebar_modulo not in menu_usuario:
    st.session_state.sidebar_modulo = menu_usuario[0] if menu_usuario else "🏠  Panel de Control"

modulo = st.sidebar.selectbox(
    "Seleccione un módulo",
    menu_usuario,
    key="sidebar_modulo"
)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

st.sidebar.divider()

st.sidebar.write("Usuario")
st.sidebar.write(st.session_state.user_name)
st.sidebar.write(st.session_state.user_role)

if st.sidebar.button(
    "Cerrar sesión",
    use_container_width=True
):

    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.user_role = ""
    st.session_state.user_email = ""
    st.session_state.user_gender = ""

    st.rerun()

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

st.sidebar.markdown(
    "<div style='font-size:0.65rem;color:rgba(13,43,82,0.35);text-align:center;'>"
    "Gestión Biomédica v1.0<br>© 2025 SPORTMEDS Centro Médico</div>",
    unsafe_allow_html=True
)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style='padding: 0.2rem 0;'>
    <div style='font-size:0.67rem;color:rgba(13,43,82,0.5);
                text-transform:uppercase;letter-spacing:.08em;'>Usuario</div>
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
    return dict(height=h, margin=dict(l=0, r=0, t=4, b=0),
                plot_bgcolor="white", paper_bgcolor="white")

from components.topbar import topbar

# ══════════════════════════════════════════
# MÓDULO: PANEL DE CONTROL
# ══════════════════════════════════════════
if "Panel" in modulo:
    topbar("Panel de Control", "Panel de Control")

    if normalize_role(st.session_state.user_role) == "Ingeniero biomédico/a":
        try:
            tv_data = supabase.table("Tecnovigilancia").select("*").execute().data or []
            if tv_data:
                df_tv = pd.DataFrame(tv_data)
                gestionados = len(df_tv[
                    df_tv["causa_codigo"].notna() &
                    (df_tv["causa_codigo"].astype(str).str.strip() != "")
                ]) if "causa_codigo" in df_tv.columns else 0
                pendientes = len(df_tv) - gestionados
            else:
                pendientes = 0
        except Exception:
            pendientes = 0

        if pendientes > 0:
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, #bf0606 0%, #700909 100%); border: 1px solid #f39c12; border-radius: 12px; padding: 0.95rem 1rem; margin-bottom: 1rem;">
                <div style="font-weight:700; color:#ffffff;">🔔 Recordatorio de tecnovigilancia</div>
                <div style="margin-top:0.25rem; color:#ffffff;">Tienes <b>{pendientes}</b> caso(s) pendiente(s) por dar solución.</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("📋 Ir a Casos reportados", key="btn_ir_casos_pendientes"):
                st.session_state.go_to_module = "📋  Casos reportados"
                st.rerun()

    try:
        inv_data = supabase.table("Inventario").select("*").execute().data
        df_inv   = pd.DataFrame(inv_data) if inv_data else pd.DataFrame()
        total_equipos  = len(df_inv)
        riesgo_alto    = len(df_inv[df_inv["clase_riesgo"] == "Clase III"]) if not df_inv.empty and "clase_riesgo" in df_inv.columns else 0
        fuera_servicio = len(df_inv[df_inv["estado"].str.contains("Fuera", na=False)]) if not df_inv.empty and "estado" in df_inv.columns else 0
    except:
        total_equipos = riesgo_alto = fuera_servicio = 0
        df_inv = pd.DataFrame()

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

    c4, c5 = st.columns([1.6, 1])

    with c4:
        st.markdown('<div class="card"><div class="card-title">Eventos tecnovigilancia — últimos 30 días</div>', unsafe_allow_html=True)
        dias       = [(date.today()-timedelta(days=i)).strftime("%Y-%m-%d") for i in range(29,-1,-1)]
        dias_label = [(date.today()-timedelta(days=i)).strftime("%d/%m")    for i in range(29,-1,-1)]
        try:
            tv_todos = supabase.table("Tecnovigilancia").select("fecha_evento").execute().data
            conteo_dias = {d: 0 for d in dias}
            if tv_todos:
                for row in tv_todos:
                    f = row.get("fecha_evento","")
                    if f and f[:10] in conteo_dias:
                        conteo_dias[f[:10]] += 1
            valores = list(conteo_dias.values())
        except:
            valores = [0] * 30

        fig4 = go.Figure(go.Scatter(
            x=dias_label, y=valores, mode="lines+markers",
            line=dict(color="#1a8fd1", width=2),
            marker=dict(color="#0D2B52", size=5),
            fill="tozeroy", fillcolor="rgba(26,143,209,0.07)"
        ))
        lay4 = base_layout(210)
        lay4.update(xaxis=dict(showgrid=False, tickangle=-45, tickfont_size=8,
                               tickvals=dias_label[::5], ticktext=dias_label[::5]),
                    yaxis=dict(gridcolor="#f0f4f9", tickfont_size=10, dtick=1))
        fig4.update_layout(lay4)
        st.plotly_chart(fig4, use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    with c5:
        st.markdown('<div class="card"><div class="card-title">Últimos equipos registrados</div>', unsafe_allow_html=True)
        if not df_inv.empty:
            cols    = ["numero_inventario","descripcion","servicio","estado"]
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
    inventario_view()

# ══════════════════════════════════════════
# MÓDULO: TECNOVIGILANCIA
# Secciones A, B, C, D, F  (solo el reportante)
# ══════════════════════════════════════════
elif "Tecnovigilancia" in modulo:
    tecnovigilancia_view()
    
# ══════════════════════════════════════════
# MÓDULO: CASOS REPORTADOS
# ══════════════════════════════════════════
elif "Casos Reportados" in modulo:
    casos_view()
    
# ══════════════════════════════════════════
# MÓDULO: GESTIÓN DE RIESGOS
# ══════════════════════════════════════════
elif "Riesgos" in modulo:
    topbar("Gestión de Riesgos", "Gestión de Riesgos")
    ce, cc = st.columns([1, 1.4])

    with ce:
        st.markdown('<div class="card"><div class="card-title">Evaluación de riesgo (AMEF)</div>',
                    unsafe_allow_html=True)
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
        st.markdown('<div class="card"><div class="card-title">Distribución de riesgo por servicio</div>',
                    unsafe_allow_html=True)
        srvs  = ["UCI","Urgencias","Hospitalización","Consulta ext."]
        fig_r = go.Figure()
        fig_r.add_bar(name="🔴 Alto",  x=srvs, y=[7,6,3,2],     marker_color="#e74c3c")
        fig_r.add_bar(name="🟡 Medio", x=srvs, y=[18,15,22,10],  marker_color="#e67e22")
        fig_r.add_bar(name="🟢 Bajo",  x=srvs, y=[43,31,64,24],  marker_color="#27ae60")
        lay_r = base_layout(270)
        lay_r.update(barmode="stack",
                     legend=dict(orientation="h", y=1.05, x=1, xanchor="right", font_size=10),
                     xaxis=dict(showgrid=False, tickfont_size=11),
                     yaxis=dict(gridcolor="#f0f4f9"))
        fig_r.update_layout(lay_r)
        st.plotly_chart(fig_r, use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card"><div class="card-title">Equipos con riesgo alto — Seguimiento</div>',
                unsafe_allow_html=True)
    try:
        riesgo_data = supabase.table("Riesgos").select("*").order("npr", desc=True).execute().data
        if riesgo_data:
            df_r2   = pd.DataFrame(riesgo_data)
            cols    = ["equipo","servicio","npr","nivel_riesgo","fecha_evaluacion","accion_requerida"]
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
                tipo_m  = st.selectbox("Tipo", [
                    "Preventivo","Correctivo","Calibración","Verificación metrológica"
                ])
                fecha_m = st.date_input("Fecha programada", value=date.today())
            with c2:
                tecnico_m   = st.text_input("Técnico responsable")
                prioridad_m = st.selectbox("Prioridad", ["🔴 Alta","🟡 Media","🟢 Baja"])
                costo_m     = st.number_input("Costo estimado (COP)", min_value=0, step=10000)
            with c3:
                servicio_m = st.selectbox("Servicio", [
                    "UCI","Urgencias","Hospitalización","Consulta externa"
                ])
                duracion_m = st.number_input("Duración estimada (h)",
                                             min_value=0.5, max_value=48.0,
                                             step=0.5, value=2.0)
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
            st.markdown('<div class="card"><div class="card-title">Cumplimiento preventivo</div>',
                        unsafe_allow_html=True)
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
            st.markdown('<div class="card"><div class="card-title">MTBF por servicio (días)</div>',
                        unsafe_allow_html=True)
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
            st.markdown('<div class="card"><div class="card-title">Distribución por tipo</div>',
                        unsafe_allow_html=True)
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
        st.markdown('<div class="card"><div class="card-title">Historial de mantenimientos</div>',
                    unsafe_allow_html=True)
        try:
            mant_data = supabase.table("Mantenimiento").select("*").execute().data
            if mant_data:
                df_mant = pd.DataFrame(mant_data)
                cols    = ["equipo","tipo_mantenimiento","fecha_programada",
                           "tecnico","costo","estado"]
                cols_ok = [c for c in cols if c in df_mant.columns]
                st.dataframe(df_mant[cols_ok], use_container_width=True, hide_index=True)
            else:
                st.info("No hay mantenimientos registrados aún.")
        except Exception as e:
            st.error(f"❌ Error al cargar historial: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
