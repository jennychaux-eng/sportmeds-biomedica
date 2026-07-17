import streamlit as st
import pandas as pd
from datetime import date
from config.config import supabase
from components.topbar import topbar

from config.config import (
    supabase,
    get_fecha_local,
)

def render():
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
                fecha_evento = st.date_input(
                    "D1. Fecha del evento / incidente *",
                    value=get_fecha_local()
                )
            with cd2:
                fecha_reporte = get_fecha_local()
                st.text_input(
                    "D2. Fecha de elaboración del reporte",
                    value=fecha_reporte.strftime("%d/%m/%Y"),
                    disabled=True
                )
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
                rep_nombre = st.text_input(
                    "F1. Nombre completo *",
                    value=st.session_state.get("user_name", st.session_state.get("reg_nombre", "")),
                    disabled=True
                )
                rep_prof   = st.text_input(
                    "F2. Profesión *",
                    value=st.session_state.get("user_profesion", st.session_state.get("reg_profesion", "")),
                    placeholder="ej. Médico, Enfermero, Ing. Biomédico",
                    disabled=True
                )
                rep_org    = st.text_input(
                    "F3. Organización o área a la que pertenece",
                    value=st.session_state.get("user_area", st.session_state.get("reg_area", "")),
                    disabled=True
                )
            with cf2:
                rep_dir   = st.text_input(
                    "F4. Dirección de la organización",
                    value="Cra. 103 #13a-23",
                    disabled=True
                )
                rep_tel   = st.text_input(
                    "F5. Teléfono de contacto",
                    value=st.session_state.get("user_telefono", st.session_state.get("reg_telefono", "")),
                    disabled=True
                )
                rep_depto = st.text_input("F6. Departamento", value="Valle del Cauca", disabled=True)
            with cf3:
                rep_ciudad = st.text_input("F7. Ciudad", value="Cali", disabled=True)
                rep_email  = st.text_input(
                    "F8. Correo electrónico institucional",
                    value=st.session_state.get("user_email", st.session_state.get("reg_correo", "")),
                    disabled=True
                )
                fecha_noti = get_fecha_local()
                st.text_input(
                    "F9. Fecha de notificación",
                    value=fecha_noti.strftime("%d/%m/%Y"),
                    disabled=True
                )
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
