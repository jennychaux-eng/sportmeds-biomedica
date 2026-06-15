import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go
import base64
from datetime import date, timedelta
from supabase import create_client, Client

def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()
        
# ─────────────────────────────────────────
# RUTAS
# ─────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "assets", "Logo_sportmeds.png")

# ─────────────────────────────────────────
# CONEXIÓN SUPABASE
# ─────────────────────────────────────────
@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_supabase()
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

def login_page():

    # =====================================================
    # ESTILOS
    # =====================================================

    background_image = get_base64_image("fondo_sportmeds.png")

    st.markdown(f"""
    <style>
    </style>
    """, unsafe_allow_html=True)

    # =====================================================
    # LAYOUT PRINCIPAL
    # =====================================================

    izquierda, derecha = st.columns([1.3, 1])

    # =====================================================
    # PANEL IZQUIERDO
    # =====================================================

    with izquierda:

        st.markdown("<br><br>", unsafe_allow_html=True)

        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=500)

        st.markdown("""
        <div class="titulo-principal">
        Sistema de Gestión<br>
        Tecnológica Hospitalaria
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="subtitulo">
        Innovación y tecnología al servicio
        de tu salud y bienestar.
        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # PANEL DERECHO
    # =====================================================

    with derecha:

        st.markdown(
            '<div class="login-card">',
            unsafe_allow_html=True
        )

        tab_login, tab_register = st.tabs(
            ["Iniciar sesión", "Registrarse"]
        )

        # ======================================
        # LOGIN
        # ======================================

        with tab_login:

            email = st.text_input(
                "Correo electrónico"
            )

            password = st.text_input(
                "Contraseña",
                type="password"
            )

            if st.button(
                "Ingresar",
                use_container_width=True
            ):

                try:

                    result = (
                        supabase
                        .table("usuarios")
                        .select("*")
                        .eq("email", email)
                        .eq("password", password)
                        .execute()
                    )

                    if result.data:

                        usuario = result.data[0]

                        st.session_state.logged_in = True
                        st.session_state.user_name = usuario["nombre"]
                        st.session_state.user_role = usuario["rol"]
                        st.session_state.user_email = usuario["email"]

                        st.rerun()

                    else:

                        st.error(
                            "Usuario o contraseña incorrectos"
                        )

                except Exception as e:

                    st.error(f"Error: {e}")

        # ======================================
        # REGISTRO
        # ======================================

        with tab_register:

            nombre = st.text_input(
                "Nombre completo",
                key="reg_nombre"
            )

            correo = st.text_input(
                "Correo electrónico",
                key="reg_correo"
            )

            clave = st.text_input(
                "Contraseña",
                type="password",
                key="reg_password"
            )

            rol = st.selectbox(
                "Rol",
                [
                    "Administrador",
                    "Ingeniero Biomédico",
                    "Técnico Biomédico",
                    "Consulta"
                ]
            )

            if st.button(
                "Crear cuenta",
                use_container_width=True
            ):

                try:

                    existe = (
                        supabase
                        .table("usuarios")
                        .select("*")
                        .eq("email", correo)
                        .execute()
                    )

                    if existe.data:

                        st.warning(
                            "Ya existe una cuenta con ese correo"
                        )

                    else:

                        supabase.table(
                            "usuarios"
                        ).insert(
                            {
                                "nombre": nombre,
                                "email": correo,
                                "password": clave,
                                "rol": rol
                            }
                        ).execute()

                        st.success(
                            "Usuario creado correctamente"
                        )

                except Exception as e:

                    st.error(f"Error: {e}")

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )
                    
    # ======================================
    # REGISTRO
    # ======================================

    with tab_register:

        nombre = st.text_input(
            "Nombre completo",
            key="reg_nombre"
        )

        correo = st.text_input(
            "Correo electrónico",
            key="reg_correo"
        )

        clave = st.text_input(
            "Contraseña",
            type="password",
            key="reg_password"
        )

        rol = st.selectbox(
            "Rol",
            [
                "Administrador",
                "Ingeniero Biomédico",
                "Técnico Biomédico",
                "Consulta"
            ]
        )

        if st.button(
            "Crear cuenta",
            use_container_width=True
        ):

            try:

                existe = (
                    supabase
                    .table("usuarios")
                    .select("*")
                    .eq("email", correo)
                    .execute()
                )

                if existe.data:

                    st.warning(
                        "Ya existe una cuenta con ese correo"
                    )

                else:

                    supabase.table(
                        "usuarios"
                    ).insert(
                        {
                            "nombre": nombre,
                            "email": correo,
                            "password": clave,
                            "rol": rol
                        }
                    ).execute()

                    st.success(
                        "Usuario creado correctamente"
                    )

            except Exception as e:

                st.error(f"Error: {e}")
                
st.markdown('</div>', unsafe_allow_html=True)
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
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

* { font-family: 'DM Sans', sans-serif !important; }

.main .block-container {
    background-color: #ffffff !important;
    padd-top: 1.2rem !important;
    max-width: 100% !important;
}
.main { background-color: #ffffff !important; }
[data-testid="stAppViewContainer"] { background-color: #ffffff !important; }
[data-testid="stAppViewBlockContainer"] { background-color: #ffffff !important; }
section.main { background-color: #ffffff !important; }

section[data-testid="stSidebar"] {
    background: white !important;
    border-right: 1px solid #e8edf5 !important;
}
section[data-testid="stSidebar"] * { color: #0D2B52 !important; }
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

.stButton > button {
    background: linear-gradient(135deg, #0D2B52, #1a8fd1) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: opacity .2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stTextInput input, .stTextArea textarea {
    border-radius: 8px !important;
    border: 1px solid #dce5f0 !important;
}

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
    color: #0D2B52 !important;
    font-weight: 500 !important;
}

[data-testid="stTabs"] button { color: #8a9bb5 !important; }
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #0D2B52 !important;
    font-weight: 700 !important;
}

.npr-box {
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    margin-top: 0.8rem;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }

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
[data-testid="collapsedControl"]:hover { background: #1a8fd1 !important; }
[data-testid="collapsedControl"] svg,
[data-testid="collapsedControl"] span { display: none !important; }
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
# CAUSAS NTC 5736:2009 (reutilizable)
# ─────────────────────────────────────────
CAUSAS_NTC = [
    "500 — Uso anormal",
    "510 — Respuesta fisiológica anormal o inesperada",
    "520 — Falla en la alarma",
    "530 — Uso de material biológico",
    "540 — Calibración incorrecta",
    "550 — Hardware del computador",
    "560 — Contaminación durante la producción",
    "570 — Contaminación postproducción",
    "580 — Diseño inadecuado",
    "590 — Desconexión imprevista",
    "600 — Componente eléctrico defectuoso",
    "610 — Circuito eléctrico",
    "620 — Contacto eléctrico defectuoso",
    "630 — Interferencia Electromagnética (IEM)",
    "640 — Fecha de expiración vencida",
    "650 — Falso negativo",
    "660 — Falso positivo",
    "670 — Resultado falso de la prueba",
    "680 — Falla en dispositivo implantable",
    "690 — Ambiente inapropiado",
    "700 — Incompatibilidad entre dispositivos",
    "710 — Instrucciones para uso / etiquetado inadecuados",
    "720 — Escape / falla en sellado",
    "730 — Mantenimiento inadecuado",
    "740 — Falla en fabricación",
    "750 — Material de durabilidad limitada",
    "760 — Componentes mecánicos",
    "770 — Condiciones no higiénicas",
    "780 — No relacionado con el dispositivo",
    "790 — Otros",
    "800 — Empaque inadecuado",
    "810 — Anatomía / fisiología del paciente",
    "820 — Condición del paciente",
    "830 — Fuente de energía deficiente",
    "840 — Falla en medidas de protección",
    "850 — Aseguramiento de calidad en la institución",
    "860 — Radiación",
    "870 — Software inadecuado",
    "880 — Esterilización / desinfección / limpieza inadecuada",
    "890 — Condiciones de almacenamiento inapropiadas",
    "900 — Alteración, falsificación o sabotaje",
    "910 — Entrenamiento inadecuado",
    "920 — Transporte y entrega",
    "930 — Sin identificar",
    "940 — Capacidad de uso",
    "950 — Error de uso",
    "960 — Desgaste",
]

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

    "Administrador": [
        "🏠  Panel de Control",
        "📦  Inventario",
        "🔍  Tecnovigilancia",
        "📋  Casos reportados",
        "⚠️  Gestión de Riesgos",
        "🔧  Mantenimiento",
    ],

    "Ingeniero Biomédico": [
        "🏠  Panel de Control",
        "📦  Inventario",
        "🔍  Tecnovigilancia",
        "📋  Casos reportados",
        "⚠️  Gestión de Riesgos",
        "🔧  Mantenimiento",
    ],

    "Técnico Biomédico": [
        "🏠  Panel de Control",
        "🔧  Mantenimiento",
    ],

    "Consulta": [
        "🏠  Panel de Control",
    ]
}

menu_usuario = ROL_MENUS.get(
    st.session_state.user_role,
    ["🏠  Panel de Control"]
)

modulo = st.sidebar.selectbox(
    "Seleccione un módulo",
    menu_usuario
)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

st.sidebar.divider()

st.sidebar.write("Usuario")
st.sidebar.write(st.session_state.user_name)
st.sidebar.write(st.session_state.user_role)

if st.sidebar.button(
    "🚪 Cerrar sesión",
    use_container_width=True
):

    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.user_role = ""
    st.session_state.user_email = ""

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

def topbar(titulo, ruta):
    st.markdown(f"""
    <div class="topbar">
        <div>
            <div class="topbar-title">{titulo}</div>
            <div class="topbar-crumb">INICIO › {ruta}</div>
        </div>
        <div class="topbar-user">👤 &nbsp; </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# MÓDULO: PANEL DE CONTROL
# ══════════════════════════════════════════
if "Panel" in modulo:
    topbar("Panel de Control", "Panel de Control")

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
                fabricante   = st.text_input("Fabricante *")
                modelo       = st.text_input("Modelo / N° catálogo")
                numero_serie = st.text_input("N° de serie")
            with c3:
                numero_lote  = st.text_input("N° de lote")
                clase_riesgo = st.selectbox("Clase de riesgo INVIMA", [
                    "Clase I", "Clase IIa", "Clase IIb", "Clase III"
                ])
                alimentacion = st.selectbox("Alimentación eléctrica", [
                    "110V", "220V", "380V", "Trifásica", "No aplica"
                ])

            st.markdown("---")
            st.markdown("#### 📍 Ubicación y estado")
            c4, c5, c6 = st.columns(3)
            with c4:
                servicio  = st.selectbox("Servicio / Ubicación *", [
                    "UCI", "Urgencias", "Hospitalización", "Consulta externa",
                    "Imágenes diagnósticas", "Cirugía", "Laboratorio", "Rehabilitación"
                ])
                ubicacion = st.text_input("Habitación / Área específica")
            with c5:
                estado     = st.selectbox("Estado operativo *", [
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
                fecha_compra   = st.date_input("Fecha de compra",  value=date.today())
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
                            "numero_inventario":       numero_inventario,
                            "tipo_equipo":             tipo_equipo,
                            "descripcion":             descripcion,
                            "fabricante":              fabricante,
                            "modelo":                  modelo,
                            "numero_serie":            numero_serie,
                            "numero_lote":             numero_lote,
                            "clase_riesgo":            clase_riesgo,
                            "alimentacion_electrica":  alimentacion,
                            "servicio":                servicio,
                            "Ubicación":               ubicacion,
                            "estado":                  estado,
                            "proveedor_compra":        proveedor_compra,
                            "proveedor_mantenimiento": proveedor_mant,
                            "fecha_compra":            str(fecha_compra),
                            "fecha_registro":          str(fecha_registro),
                            "garantia_inicio":         str(garantia_inicio),
                            "garantia_fin":            str(garantia_fin),
                            "costo":                   float(costo),
                            "observaciones":           obs,
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
                cols_show      = ["numero_inventario","descripcion","fabricante","modelo",
                                  "clase_riesgo","servicio","estado","fecha_compra"]
                cols_available = [c for c in cols_show if c in df.columns]
                st.dataframe(df[cols_available], use_container_width=True, hide_index=True)
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
# Secciones A, B, C, D, F  (solo el reportante)
# ══════════════════════════════════════════
elif "Tecnovigilancia" in modulo:
    topbar("Tecnovigilancia", "Tecnovigilancia")

    tab_nuevo, tab_historial = st.tabs(["📋  Nuevo reporte", "📊  Historial de reportes"])

    @st.cache_data(ttl=60)
    def cargar_inventario():
        try:
            data = supabase.table("Inventario").select("*").execute().data
            return pd.DataFrame(data) if data else pd.DataFrame()
        except:
            return pd.DataFrame()

    df_inv = cargar_inventario()

    # ── TAB 1: NUEVO REPORTE ──
    with tab_nuevo:

        st.markdown('<div class="card"><div class="card-title">🔍 Selección del equipo involucrado</div>',
                    unsafe_allow_html=True)

        if df_inv.empty:
            st.warning("⚠️ No hay equipos registrados en el inventario.")
            equipo_sel = None
        else:
            opciones = ["— Seleccione un equipo —"] + [
                f"{row['numero_inventario']} — {row['descripcion']}"
                for _, row in df_inv.iterrows()
            ]
            equipo_label = st.selectbox(
                "Equipo involucrado en el evento *", opciones,
                help="Al seleccionar el equipo los campos del dispositivo se llenan automáticamente."
            )
            equipo_sel = None
            if equipo_label != "— Seleccione un equipo —":
                inv_id  = equipo_label.split(" — ")[0].strip()
                matches = df_inv[df_inv["numero_inventario"] == inv_id]
                if not matches.empty:
                    equipo_sel = matches.iloc[0]

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("form_foreia001", clear_on_submit=True):

            # ── SECCIÓN A ──
            st.markdown("#### 🏥 Lugar de ocurrencia del evento o incidente")
            ca1, ca2, ca3 = st.columns(3)
            with ca1:
                st.text_input("A1. Nombre de la institución",
                              value="SPORTMEDS Centro Médico S.A.S", disabled=True)
                st.text_input("A4. NIT", value="901.002.107-7", disabled=True)
            with ca2:
                st.text_input("A2. Departamento", value="Valle del Cauca", disabled=True)
                st.text_input("A5. Nivel de complejidad", value="2", disabled=True)
            with ca3:
                st.text_input("A3. Ciudad", value="Cali", disabled=True)
                st.text_input("A6. Naturaleza", value="Privada", disabled=True)

            st.markdown("---")

            # ── SECCIÓN B ──
            st.markdown("#### 🧑‍⚕️ Información del paciente")
            cb1, cb2, cb3, cb4 = st.columns([1.2, 0.8, 0.8, 1.5])
            with cb1:
                pac_id = st.text_input("B1. Identificación del paciente *",
                                       placeholder="Iniciales o N° historia clínica")
            with cb2:
                pac_sexo = st.selectbox("B2. Sexo *",
                                        ["— Seleccione —", "Femenino", "Masculino"])
            with cb3:
                pac_edad = st.text_input("B3. Edad *", placeholder="ej. 45 años / 3 meses")
            with cb4:
                pac_dx = st.text_input("B4. Diagnóstico inicial *",
                                       placeholder="Causa de atención que originó el uso del dispositivo")

            st.markdown("---")

            # ── SECCIÓN C ──
            st.markdown("#### 🩺 Identificación del dispositivo médico")
            st.caption("Campos autocompletados desde el inventario — no editables.")

            if equipo_sel is not None:
                nombre_generico  = str(equipo_sel.get("descripcion",      "") or "")
                nombre_comercial = str(equipo_sel.get("modelo",           "") or "")
                registro_san     = str(equipo_sel.get("clase_riesgo",     "") or "")
                lote_val         = str(equipo_sel.get("numero_lote",      "") or "")
                modelo_val       = str(equipo_sel.get("modelo",           "") or "")
                serial_val       = str(equipo_sel.get("numero_serie",     "") or "")
                fabricante_val   = str(equipo_sel.get("fabricante",       "") or "")
                importador_val   = str(equipo_sel.get("proveedor_compra", "") or "")
                area_val         = str(equipo_sel.get("servicio",         "") or "")
                num_inv_val      = str(equipo_sel.get("numero_inventario","") or "")
            else:
                nombre_generico = nombre_comercial = registro_san = ""
                lote_val = modelo_val = serial_val = ""
                fabricante_val = importador_val = area_val = num_inv_val = ""

            cc1, cc2 = st.columns(2)
            with cc1:
                st.text_input("C1. Nombre genérico del dispositivo médico",
                              value=nombre_generico, disabled=True)
                st.text_input("C3. Registro sanitario",
                              value=registro_san, disabled=True)
                st.text_input("C5. Fabricante",
                              value=fabricante_val, disabled=True)
                st.text_input("C7. Área de funcionamiento",
                              value=area_val, disabled=True)
            with cc2:
                st.text_input("C2. Nombre comercial",
                              value=nombre_comercial, disabled=True)
                c_lote, c_mod = st.columns(2)
                with c_lote:
                    st.text_input("Lote",   value=lote_val,   disabled=True)
                with c_mod:
                    st.text_input("Modelo", value=modelo_val, disabled=True)
                c_ref, c_ser = st.columns(2)
                with c_ref:
                    st.text_input("Referencia", value=modelo_val, disabled=True)
                with c_ser:
                    st.text_input("Serial",     value=serial_val, disabled=True)
                st.text_input("C6. Importador / distribuidor",
                              value=importador_val, disabled=True)
                uso_multiple = st.radio(
                    "C8. ¿El dispositivo ha sido utilizado más de una vez?",
                    ["No", "Sí"], horizontal=True
                )

            st.markdown("---")

            # ── SECCIÓN D ──
            st.markdown("#### ⚠️ Evento o incidente adverso")

            cd1, cd2, cd3 = st.columns(3)
            with cd1:
                fecha_evento = st.date_input("D1. Fecha del evento / incidente *",
                                             value=date.today())
            with cd2:
                fecha_reporte = date.today()
                st.text_input("D2. Fecha de elaboración del reporte",
                              value=fecha_reporte.strftime("%d/%m/%Y"), disabled=True)
            with cd3:
                deteccion = st.selectbox("D3. Detección del evento / incidente", [
                    "Antes del uso del dispositivo médico",
                    "Durante el uso del dispositivo médico",
                    "Después del uso del dispositivo médico"
                ])

            clasificacion = st.radio(
                "D4. Clasificación *",
                ["Evento adverso serio", "Evento adverso no serio",
                 "Incidente adverso serio", "Incidente adverso no serio"],
                horizontal=True
            )

            descripcion_ev = st.text_area(
                "D5. Descripción detallada del evento o incidente adverso *",
                height=130,
                placeholder=(
                    "Describa: estado de salud del paciente antes del evento, signos y síntomas, "
                    "condiciones relevantes (hipertensión, diabetes, alergias), "
                    "diagnóstico diferencial, curso clínico, tratamiento administrado y resultados..."
                )
            )

            st.markdown("**D6. Desenlace** — seleccione todas las que apliquen:")
            dc1, dc2, dc3 = st.columns(3)
            with dc1:
                d_muerte   = st.checkbox("Muerte")
                d_amenaza  = st.checkbox("Enfermedad o daño que amenace la vida")
            with dc2:
                d_funcion  = st.checkbox("Daño de una función o estructura corporal")
                d_hosp     = st.checkbox("Hospitalización inicial o prolongada")
            with dc3:
                d_interv   = st.checkbox("Requiere intervención médica o quirúrgica")
                d_sin_dano = st.checkbox("No hubo daño")
                d_otro     = st.checkbox("Otro")

            d_otro_cual = st.text_input(
                "Si marcó Otro, especifique el desenlace:",
                placeholder="Describa el otro desenlace aquí...",
                key="d_otro_cual_input"
            )

            st.markdown("---")

            # ── SECCIÓN F ──
            st.markdown("#### 👤 Información del reportante")

            cf1, cf2, cf3 = st.columns(3)
            with cf1:
                rep_nombre = st.text_input("F1. Nombre completo *")
                rep_prof   = st.text_input("F2. Profesión *",
                                           placeholder="ej. Médico, Enfermero, Ing. Biomédico")
                rep_org    = st.text_input("F3. Organización o área a la que pertenece")
            with cf2:
                rep_dir   = st.text_input("F4. Dirección de la organización")
                rep_tel   = st.text_input("F5. Teléfono de contacto")
                rep_depto = st.text_input("F6. Departamento", value="Valle del Cauca")
            with cf3:
                rep_ciudad = st.text_input("F7. Ciudad", value="Cali")
                rep_email  = st.text_input("F8. Correo electrónico institucional")
                fecha_noti = st.date_input("F9. Fecha de notificación", value=date.today())
                autoriza   = st.radio(
                    "F10. ¿Autoriza divulgación del origen del reporte?",
                    ["No", "Sí"], horizontal=True
                )

            st.markdown("<br>", unsafe_allow_html=True)

            submitted = st.form_submit_button("📋 Guardar reporte en base de datos",
                                              use_container_width=True)

            if submitted:
                errores = []
                if equipo_sel is None:
                    errores.append("Debe seleccionar un equipo del inventario.")
                if not pac_id:
                    errores.append("La identificación del paciente es obligatoria (B1).")
                if pac_sexo == "— Seleccione —":
                    errores.append("El sexo del paciente es obligatorio (B2).")
                if not pac_edad:
                    errores.append("La edad del paciente es obligatoria (B3).")
                if not pac_dx:
                    errores.append("El diagnóstico inicial es obligatorio (B4).")
                if not descripcion_ev:
                    errores.append("La descripción del evento es obligatoria (D5).")
                if not rep_nombre:
                    errores.append("El nombre del reportante es obligatorio (F1).")
                if not rep_prof:
                    errores.append("La profesión del reportante es obligatoria (F2).")

                if errores:
                    st.error("Por favor corrija los siguientes errores antes de guardar:")
                    for e in errores:
                        st.error(f"❌ {e}")
                else:
                    desenlaces = []
                    if d_muerte:   desenlaces.append("Muerte")
                    if d_amenaza:  desenlaces.append("Enfermedad o daño que amenace la vida")
                    if d_funcion:  desenlaces.append("Daño de una función o estructura corporal")
                    if d_hosp:     desenlaces.append("Hospitalización inicial o prolongada")
                    if d_interv:   desenlaces.append("Requiere intervención médica o quirúrgica")
                    if d_sin_dano: desenlaces.append("No hubo daño")
                    if d_otro:     desenlaces.append(f"Otro: {d_otro_cual}")

                    try:
                        data_tv = {
                            # A
                            "nombre_institucion":        "SPORTMEDS Centro Médico S.A.S",
                            "departamento":              "Valle del Cauca",
                            "ciudad":                    "Cali",
                            "nit":                       "901.002.107-7",
                            "nivel_complejidad":         "2",
                            "naturaleza":                "Privada",
                            # B
                            "paciente_identificacion":   pac_id,
                            "paciente_sexo":             pac_sexo,
                            "paciente_edad":             pac_edad,
                            "paciente_diagnostico":      pac_dx,
                            # C
                            "numero_inventario":         num_inv_val,
                            "nombre_generico":           nombre_generico,
                            "nombre_comercial":          nombre_comercial,
                            "registro_sanitario":        registro_san,
                            "lote":                      lote_val,
                            "modelo":                    modelo_val,
                            "referencia":                modelo_val,
                            "serial":                    serial_val,
                            "fabricante":                fabricante_val,
                            "importador":                importador_val,
                            "area_funcionamiento":       area_val,
                            "uso_multiple":              uso_multiple == "Sí",
                            # D
                            "fecha_evento":              str(fecha_evento),
                            "fecha_elaboracion_reporte": str(fecha_reporte),
                            "deteccion":                 deteccion,
                            "clasificacion":             clasificacion,
                            "descripcion_evento":        descripcion_ev,
                            "desenlace":                 desenlaces,
                            "desenlace_otro":            d_otro_cual,
                            # F
                            "reportante_nombre":         rep_nombre,
                            "reportante_profesion":      rep_prof,
                            "reportante_organizacion":   rep_org,
                            "reportante_direccion":      rep_dir,
                            "reportante_telefono":       rep_tel,
                            "reportante_departamento":   rep_depto,
                            "reportante_ciudad":         rep_ciudad,
                            "reportante_email":          rep_email,
                            "fecha_notificacion":        str(fecha_noti),
                            "autoriza_divulgacion":      autoriza == "Sí",
                        }

                        supabase.table("Tecnovigilancia").insert(data_tv).execute()

                        st.success(
                            f"✅ Reporte guardado para **{nombre_generico}** "
                            f"(Inventario: {num_inv_val}). "
                            f"El Ing. Biomédico tomará acción en **📋 Casos reportados**."
                        )

                        if clasificacion in ["Evento adverso serio", "Incidente adverso serio"]:
                            st.warning(
                                "⚠️ **EVENTO / INCIDENTE SERIO.**  \n"
                                "Notificar al INVIMA dentro de las **72 horas** siguientes.  \n"
                                "📧 tecnovigilancia@invima.gov.co  |  📠 Fax: 4235656 ext. 104"
                            )

                        st.balloons()

                    except Exception as e:
                        st.error(f"❌ Error al guardar en Supabase: {e}")

    # ── TAB 2: HISTORIAL ──
    with tab_historial:
        st.markdown('<div class="card"><div class="card-title">Reportes registrados</div>',
                    unsafe_allow_html=True)
        try:
            tv_data = supabase.table("Tecnovigilancia").select("*").order("created_at", desc=True).execute().data

            if tv_data:
                df_tv     = pd.DataFrame(tv_data)
                total     = len(df_tv)
                serios    = len(df_tv[df_tv["clasificacion"].str.contains("serio", case=False, na=False)]) \
                            if "clasificacion" in df_tv.columns else 0
                no_serios = total - serios

                kc1, kc2, kc3, kc4 = st.columns(4)
                kc1.metric("Total reportes", total)
                kc2.metric("Serios", serios,
                           delta="Requieren notif. INVIMA <72h" if serios > 0 else None,
                           delta_color="inverse")
                kc3.metric("No serios", no_serios)
                if "fecha_evento" in df_tv.columns and not df_tv["fecha_evento"].isna().all():
                    kc4.metric("Último evento", str(df_tv["fecha_evento"].dropna().iloc[0])[:10])

                st.markdown("<br>", unsafe_allow_html=True)

                cols_show = ["created_at","numero_inventario","nombre_generico",
                             "clasificacion","fecha_evento","deteccion",
                             "desenlace","reportante_nombre","reportante_profesion"]
                cols_ok   = [c for c in cols_show if c in df_tv.columns]
                st.dataframe(
                    df_tv[cols_ok].rename(columns={
                        "created_at":          "Fecha registro",
                        "numero_inventario":   "Inventario",
                        "nombre_generico":     "Dispositivo",
                        "clasificacion":       "Clasificación",
                        "fecha_evento":        "Fecha evento",
                        "deteccion":           "Detección",
                        "desenlace":           "Desenlace",
                        "reportante_nombre":   "Reportante",
                        "reportante_profesion":"Profesión",
                    }),
                    use_container_width=True, hide_index=True
                )

                if "clasificacion" in df_tv.columns:
                    cl_counts  = df_tv["clasificacion"].value_counts()
                    col_colors = {
                        "Evento adverso serio":       "#e74c3c",
                        "Evento adverso no serio":    "#e67e22",
                        "Incidente adverso serio":    "#9b59b6",
                        "Incidente adverso no serio": "#1a8fd1",
                    }
                    fig_cl = go.Figure(go.Bar(
                        x=cl_counts.index.tolist(),
                        y=cl_counts.values.tolist(),
                        marker_color=[col_colors.get(c, "#8a9bb5") for c in cl_counts.index],
                        text=cl_counts.values.tolist(), textposition="outside"
                    ))
                    fig_cl.update_layout(
                        height=240, margin=dict(l=0,r=0,t=4,b=0),
                        plot_bgcolor="white", paper_bgcolor="white",
                        xaxis=dict(showgrid=False, tickfont_size=10),
                        yaxis=dict(gridcolor="#f0f4f9", tickfont_size=10, dtick=1)
                    )
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<div class="card-title">Reportes por clasificación</div>',
                                unsafe_allow_html=True)
                    st.plotly_chart(fig_cl, use_container_width=True, config=PLOT_CFG)

                csv = df_tv.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Exportar todos los reportes a CSV", csv,
                                   "tecnovigilancia_reportes.csv", "text/csv")
            else:
                st.info("No hay reportes registrados aún. Usa la pestaña 📋 Nuevo reporte.")

        except Exception as e:
            st.error(f"❌ Error al cargar historial: {e}")

        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# MÓDULO: CASOS REPORTADOS
# Exclusivo Ing. Biomédico — Sección E
# ══════════════════════════════════════════
elif "Casos reportados" in modulo:
    topbar("Casos reportados — Gestión Ing. Biomédico", "Casos reportados")

    try:
        tv_data = supabase.table("Tecnovigilancia").select("*").order("created_at", desc=True).execute().data
    except Exception as e:
        st.error(f"❌ Error al cargar casos: {e}")
        tv_data = []

    if not tv_data:
        st.info("No hay casos reportados aún.")
    else:
        df_tv = pd.DataFrame(tv_data)

        # ── KPIs ──
        total       = len(df_tv)
        serios      = len(df_tv[df_tv["clasificacion"].str.contains("serio", case=False, na=False)]) \
                      if "clasificacion" in df_tv.columns else 0
        gestionados = len(df_tv[
            df_tv["causa_codigo"].notna() &
            (df_tv["causa_codigo"].astype(str).str.strip() != "")
        ]) if "causa_codigo" in df_tv.columns else 0
        pendientes  = total - gestionados

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total casos", total)
        k2.metric("Serios", serios,
                  delta="Notif. INVIMA <72h" if serios > 0 else None,
                  delta_color="inverse")
        k3.metric("⏳ Pendientes", pendientes,
                  delta="Requieren acción" if pendientes > 0 else None,
                  delta_color="inverse")
        k4.metric("✅ Gestionados", gestionados)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Tabla resumen ──
        st.markdown('<div class="card"><div class="card-title">Listado de casos reportados</div>',
                    unsafe_allow_html=True)

        cols_tabla = ["id","created_at","numero_inventario","nombre_generico",
                      "clasificacion","fecha_evento","reportante_nombre","causa_codigo"]
        cols_ok    = [c for c in cols_tabla if c in df_tv.columns]
        df_tabla   = df_tv[cols_ok].copy()

        if "causa_codigo" in df_tabla.columns:
            df_tabla["Estado gestión"] = df_tabla["causa_codigo"].apply(
                lambda x: "✅ Gestionado"
                if (x is not None and str(x).strip() != "")
                else "⏳ Pendiente"
            )

        st.dataframe(
            df_tabla.rename(columns={
                "id":                "ID",
                "created_at":        "Fecha registro",
                "numero_inventario": "Inventario",
                "nombre_generico":   "Dispositivo",
                "clasificacion":     "Clasificación",
                "fecha_evento":      "Fecha evento",
                "reportante_nombre": "Reportante",
                "causa_codigo":      "Cód. causa (E1)",
            }),
            use_container_width=True, hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Panel de gestión sección E ──
        st.markdown('<div class="card"><div class="card-title">🔧 E. Gestión realizada — Ing. Biomédico</div>',
                    unsafe_allow_html=True)

        opciones_casos = [
            f"{str(row['id'])[:8]}... | {row.get('nombre_generico','—')} | "
            f"{row.get('fecha_evento','—')} | {row.get('clasificacion','—')}"
            for _, row in df_tv.iterrows()
        ]
        caso_label = st.selectbox("Seleccione el caso a gestionar", opciones_casos)
        caso_idx   = opciones_casos.index(caso_label)
        caso_sel   = df_tv.iloc[caso_idx]
        caso_id    = caso_sel["id"]

        # ── Resumen del caso ──
        st.markdown('<div class="card" style="margin-bottom:0.8rem;"><div class="card-title">Resumen del caso seleccionado</div>', unsafe_allow_html=True)
        r1, r2, r3, r4 = st.columns(4)
        r1.info(f"**Dispositivo:** {caso_sel.get('nombre_generico','—')}")
        r2.info(f"**Clasificación:** {caso_sel.get('clasificacion','—')}")
        r3.info(f"**Fecha evento:** {caso_sel.get('fecha_evento','—')}")
        r4.info(f"**Reportante:** {caso_sel.get('reportante_nombre','—')}")
        st.markdown("**Descripción del evento:**")
        st.write(caso_sel.get("descripcion_evento", "—"))
        desenlace_val = caso_sel.get("desenlace", [])
        if desenlace_val:
            texto_des = ", ".join(desenlace_val) if isinstance(desenlace_val, list) else str(desenlace_val)
            st.markdown(f"**Desenlace:** {texto_des}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Valores actuales para pre-llenar ──
        causa_actual      = str(caso_sel.get("causa_codigo",         "") or "")
        causa_desc_actual = str(caso_sel.get("causa_probable",       "") or "")
        acciones_actual   = str(caso_sel.get("acciones_correctivas", "") or "")
        rep_imp_actual    = bool(caso_sel.get("reporto_importador",   False))
        disp_disp_actual  = bool(caso_sel.get("dispositivo_disponible", False))
        disp_env_actual   = bool(caso_sel.get("dispositivo_enviado",    False))

        causa_index = 0
        for i, c in enumerate(CAUSAS_NTC):
            if c.startswith(causa_actual):
                causa_index = i
                break

        # ── Formulario E ──
        with st.form("form_gestion_e"):

            st.markdown("##### E1. Causa probable del evento / incidente (NTC 5736:2009)")
            ge1, ge2 = st.columns(2)

            with ge1:
                causa_codigo = st.selectbox("Código y causa", CAUSAS_NTC, index=causa_index)
                causa_descripcion = st.text_area(
                    "Descripción de la causa probable",
                    value=causa_desc_actual,
                    height=110,
                    placeholder="Describa la causa identificada según el análisis realizado..."
                )

            with ge2:
                acciones = st.text_area(
                    "E2. Acciones correctivas y preventivas iniciadas",
                    value=acciones_actual,
                    height=110,
                    placeholder="Acciones implementadas para corregir y prevenir la recurrencia..."
                )

            st.markdown("---")

            eg1, eg2, eg3 = st.columns(3)

            with eg1:
                st.markdown("**E3. ¿Reportó al importador / distribuidor?**")
                reporto_imp = st.radio(
                    "Reportó al importador",
                    ["No", "Sí"],
                    index=1 if rep_imp_actual else 0,
                    horizontal=True,
                    label_visibility="collapsed"
                )
                fecha_rep_imp = st.date_input("Fecha del reporte al importador",
                                              value=date.today())

            with eg2:
                st.markdown("**E4. ¿Dispositivo disponible para evaluación?**")
                st.caption("No enviar al INVIMA")
                disp_disponible = st.radio(
                    "Dispositivo disponible",
                    ["No", "Sí"],
                    index=1 if disp_disp_actual else 0,
                    horizontal=True,
                    label_visibility="collapsed"
                )

            with eg3:
                st.markdown("**E5. ¿Se envió el dispositivo al distribuidor / importador?**")
                disp_enviado = st.radio(
                    "Dispositivo enviado",
                    ["No", "Sí"],
                    index=1 if disp_env_actual else 0,
                    horizontal=True,
                    label_visibility="collapsed"
                )
                fecha_envio_disp = st.date_input("Fecha de envío", value=date.today())

            st.markdown("<br>", unsafe_allow_html=True)

            guardar_gestion = st.form_submit_button(
                "💾 Guardar gestión (Sección E)",
                use_container_width=True
            )

            if guardar_gestion:
                if not causa_descripcion.strip():
                    st.error("❌ La descripción de la causa probable es obligatoria.")
                elif not acciones.strip():
                    st.error("❌ Las acciones correctivas y preventivas son obligatorias.")
                else:
                    try:
                        update_data = {
                            "causa_codigo":             causa_codigo.split(" — ")[0],
                            "causa_probable":           causa_descripcion,
                            "acciones_correctivas":     acciones,
                            "reporto_importador":       reporto_imp == "Sí",
                            "fecha_reporte_importador": str(fecha_rep_imp) if reporto_imp == "Sí" else None,
                            "dispositivo_disponible":   disp_disponible == "Sí",
                            "dispositivo_enviado":      disp_enviado == "Sí",
                            "fecha_envio_dispositivo":  str(fecha_envio_disp) if disp_enviado == "Sí" else None,
                        }
                        supabase.table("Tecnovigilancia").update(update_data).eq("id", caso_id).execute()
                        st.success(
                            f"✅ Gestión guardada correctamente para el caso de "
                            f"**{caso_sel.get('nombre_generico','—')}**."
                        )
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error al guardar la gestión: {e}")

        st.markdown('</div>', unsafe_allow_html=True)

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
