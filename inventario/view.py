# ══════════════════════════════════════════
# MÓDULO: INVENTARIO
# ══════════════════════════════════════════
import streamlit as st
import pandas as pd

from datetime import date

from config.config import supabase
from components.topbar import topbar

elif "Inventario" in modulo:

def render():
    
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

