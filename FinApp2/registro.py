import streamlit as st
from utils_db import cargar_subcategorias_db, guardar_transaccion_db, cargar_cuentas_db

st.set_page_config(page_title="Registrar Transacción", layout="centered")
st.title("📝 Registro de nueva transacción")

# Cargar opciones dinámicas
cuentas = cargar_cuentas_db()
subcategorias = cargar_subcategorias_db()

# Formulario
with st.form("registro_formulario"):
    fecha = st.date_input("Fecha")
    tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
    cuenta = st.selectbox("Cuenta", cuentas if cuentas else [""])
    categoria = st.text_input("Categoría")
    subcategoria = st.selectbox("Subcategoría", subcategorias if subcategorias else [""])
    monto = st.number_input("Monto", min_value=0.0, step=0.01)
    descripcion = st.text_input("Descripción")
    proyecto = st.text_input("Proyecto")
    uso = st.text_input("Uso")

    enviado = st.form_submit_button("Guardar transacción")

    if enviado:
        if not categoria or not cuenta or monto <= 0:
            st.error("⚠️ Por favor completá todos los campos obligatorios.")
        else:
            guardar_transaccion_db(
                fecha.strftime("%Y-%m-%d"),
                tipo,
                cuenta,
                categoria,
                subcategoria,
                monto,
                descripcion,
                proyecto,
                uso
            )
            st.success("✅ Transacción registrada correctamente")
