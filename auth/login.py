import streamlit as st
import os

from config.config import (
    LOGO_PATH,
    supabase,
    get_base64_image
)

def login_page():

    # =====================================================
    # ESTILOS
    # =====================================================

    background_image = get_base64_image(
        "fondo_sportmeds.png"
    )

    st.markdown(f"""
<style>

.stApp {{
    background-image: url("data:image/png;base64,{background_image}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
    right: 2rem;
}}

.login-card {{
    background: rgba(255,255,255,0.98);
    padding: 36px 34px;
    border-radius: 18px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.18);
    /* larger rectangular background on the right */
    position: absolute;
    right: 1%;
    top: 10%;
    max-width: 2500px;
    min-height: 500px;
    width: 100%;
    box-sizing: border-box;
    z-index: 0;
}}

.titulo-principal {{
    font-size: 2.2rem;
    font-weight: 700;
    color: #000000;
    margin-top: 30px;
}}

.subtitulo {{
    font-size: 1.1rem;
    color: #6b7280;
    margin-top: 15px;
}}

/* Ensure Streamlit interactive controls render above the white card */
[data-testid="stTabs"],
.stTextInput,
.stButton > button,
.stSelectbox,
.stTextArea textarea {{
    position: relative;
    z-index: 1;
}}

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
    # ======================================================

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
                        st.session_state.user_profesion = usuario.get("profesion", "")
                        st.session_state.user_telefono = usuario.get("telefono", "")
                        st.session_state.user_area = usuario.get("area", "")
                        st.session_state.user_gender = usuario.get("genero", "")

                        st.rerun()

                    else:

                        st.error(
                            "Usuario o contraseña incorrectos"
                        )

                except Exception as e:

                    st.error(f"Error: {e}")

        with tab_register:

            col1, col2 = st.columns(2)

            with col1:
                nombre = st.text_input(
                    "Nombre completo",
                    key="reg_nombre"
                )

                profesion = st.text_input(
                    "Profesión",
                    key="reg_profesion"
                )

                telefono = st.text_input(
                    "Telefono de contacto",
                    key="reg_telefono"
                )

                correo = st.text_input(
                    "Correo",
                    key="reg_correo"
                )

            with col2:
                area = st.text_input(
                    "Área a la que pertenece",
                    key="reg_area"
                )

                clave = st.text_input(
                    "Contraseña",
                    type="password",
                    key="reg_password"
                )

                genero = st.selectbox(
                    "Género",
                    [
                        "Femenino",
                        "Masculino",
                        "Otro",
                    ],
                    key="reg_genero"
                )

                rol = st.selectbox(
                    "Rol",
                    [
                        "Gerente",
                        "Ingeniero biomédico/a",
                        "Cirujano/a",
                        "Médico/a",
                        "Enfermero/a",
                        "Instrumentador quirurgico/a",
                        "Encargado del mantenimiento",
                    ],
                    key="reg_rol"
                )

            if st.button(
                "Crear cuenta",
                use_container_width=True,
                key="btn_registro"
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
                                "profesion": profesion,
                                "telefono": telefono,
                                "email": correo,
                                "area": area,
                                "password": clave,
                                "genero": genero,
                                "rol": rol
                            }
                        ).execute()

                        st.session_state.user_name = nombre
                        st.session_state.user_email = correo
                        st.session_state.user_profesion = profesion
                        st.session_state.user_telefono = telefono
                        st.session_state.user_area = area

                        st.success(
                            "Usuario creado correctamente"
                        )

                except Exception as e:

                    st.error(f"Error: {e}")

        st.markdown('</div>', unsafe_allow_html=True)
