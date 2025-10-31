import streamlit as st
import pandas as pd
from utils_db import cargar_cuentas_db, cargar_subcategorias_db, guardar_transaccion_db, cargar_transacciones_db

st.set_page_config(page_title="Registrar Transacción", layout="centered")
st.title("📝 Registro de nueva transacción")

# Cargar datos base
transacciones = cargar_transacciones_db()
df = pd.DataFrame(transacciones)
df["fecha"] = pd.to_datetime(df["fecha"])

# Paso 1: elegir uso
uso = st.radio("¿Esta transacción es de tipo…", ["Negocio", "Personal"])

# Filtrar categorías según uso
categorias_filtradas = sorted(df[df["uso"] == uso]["categoria"].dropna().unique().tolist())
subcategorias_existentes = sorted(df[df["uso"] == uso]["subcategoria"].dropna().unique().tolist())
cuentas_existentes = sorted(df[df["uso"] == uso]["cuenta"].dropna().unique().tolist())

# Formulario
with st.form("registro_formulario"):
    fecha = st.date_input("Fecha")
    tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])

    cuenta = st.selectbox("Cuenta existente", [""] + cuentas_existentes)
    cuenta_nueva = st.text_input("O escribe una nueva cuenta")

    categoria = st.selectbox("Categoría", [""] + categorias_filtradas)
    categoria_nueva = st.text_input("O escribe una nueva categoría")

    subcategoria = st.selectbox("Subcategoría existente", [""] + subcategorias_existentes)
    subcategoria_nueva = st.text_input("O escribe una nueva subcategoría")

    monto = st.number_input("Monto", min_value=0.0, step=0.01)
    descripcion = st.text_input("Descripción")
    proyecto = st.text_input("Proyecto")

    enviado = st.form_submit_button("Guardar transacción")

    if enviado:
        cuenta_final = cuenta_nueva if cuenta_nueva else cuenta
        categoria_final = categoria_nueva if categoria_nueva else categoria
        subcategoria_final = subcategoria_nueva if subcategoria_nueva else subcategoria

        if not cuenta_final or not categoria_final or monto <= 0:
            st.error("⚠️ Por favor completá todos los campos obligatorios.")
        else:
            guardar_transaccion_db(
                fecha.strftime("%Y-%m-%d"),
                tipo,
                cuenta_final,
                categoria_final,
                subcategoria_final,
                monto,
                descripcion,
                proyecto,
                uso
            )
            st.success("✅ Transacción registrada correctamente")
