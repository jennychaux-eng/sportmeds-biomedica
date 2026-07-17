
def render():
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
                      "clasificacion","fecha_evento","reportante_nombre",
                      "descripcion_evento","causa_codigo"]
        cols_ok    = [c for c in cols_tabla if c in df_tv.columns]
        df_tabla   = df_tv[cols_ok].copy()

        if "causa_codigo" in df_tabla.columns:
            df_tabla["Estado gestión"] = df_tabla["causa_codigo"].apply(
                lambda x: "✅ Gestionado"
                if (x is not None and str(x).strip() != "")
                else "⏳ Pendiente"
            )

        if "descripcion_evento" in df_tabla.columns:
            df_tabla["D5. Descripción detallada del evento o incidente adverso *"] = df_tabla["descripcion_evento"].apply(
                lambda x: (str(x)[:180] + "...") if isinstance(x, str) and len(x) > 180 else (x if x is not None else "")
            )

        df_tabla_renombrada = df_tabla.rename(columns={
            "id":                "ID",
            "created_at":        "Fecha registro",
            "numero_inventario": "Inventario",
            "nombre_generico":   "Dispositivo",
            "clasificacion":     "Clasificación",
            "fecha_evento":      "Fecha evento",
            "reportante_nombre": "Reportante",
            "causa_codigo":      "Cód. causa (E1)",
        })

        if "D5. Descripción detallada del evento o incidente adverso *" in df_tabla_renombrada.columns:
            df_tabla_renombrada = df_tabla_renombrada.rename(columns={
                "D5. Descripción detallada del evento o incidente adverso *": "D5. Descripción detallada del evento o incidente adverso *"
            })

        st.dataframe(
            df_tabla_renombrada,
            use_container_width=True, hide_index=True,
            column_config={
                "D5. Descripción detallada del evento o incidente adverso *": st.column_config.TextColumn(
                    "D5. Descripción detallada del evento o incidente adverso *",
                    width="large"
                ),
                "Clasificación": st.column_config.TextColumn(width="medium"),
                "Reportante": st.column_config.TextColumn(width="medium"),
            }
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Panel de gestión sección E ──
        st.markdown('<div class="card"><div class="card-title">🔧 E. Gestión realizada — Ing. Biomédico</div>',
                    unsafe_allow_html=True)

        df_pendientes = df_tv.copy()
        if "causa_codigo" in df_pendientes.columns:
            df_pendientes = df_pendientes[
                df_pendientes["causa_codigo"].isna() |
                df_pendientes["causa_codigo"].astype(str).str.strip().eq("")
            ]

        if df_pendientes.empty:
            st.info("No hay casos pendientes por gestionar.")
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop()

        opciones_casos = [
            f"{str(row['id'])[:8]}... | {row.get('nombre_generico','—')} | "
            f"{row.get('fecha_evento','—')} | {row.get('clasificacion','—')}"
            for _, row in df_pendientes.iterrows()
        ]
        caso_label = st.selectbox("Seleccione el caso a gestionar", opciones_casos)
        caso_idx   = opciones_casos.index(caso_label)
        caso_sel   = df_pendientes.iloc[caso_idx]
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

