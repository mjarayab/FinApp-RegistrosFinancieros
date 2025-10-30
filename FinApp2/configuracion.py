import streamlit as st
import pandas as pd
from utils_db import (
    cargar_cuentas_db, cargar_subcategorias_db,
    guardar_cuenta_db, guardar_subcategoria_db,
    cuenta_existe, subcategoria_existe
)

st.set_page_config(page_title="Configuración", layout="wide")
st.title("⚙️ Configuración de FinApp2")

# --- CUENTAS ---
st.subheader("🏦 Cuentas registradas")
cuentas = cargar_cuentas_db()
df_cuentas = pd.DataFrame(cuentas)
st.dataframe(df_cuentas, use_container_width=True)

with st.expander("➕ Agregar nueva cuenta"):
    nombre = st.text_input("Nombre de la cuenta")
    tipo = st.selectbox("Tipo", ["Efectivo", "Banco", "Tarjeta", "Crédito", "Otro"])
    saldo_inicial = st.number_input("Saldo inicial", step=100.0)
    moneda = st.selectbox("Moneda", ["CRC", "USD", "EUR"])
    uso = st.selectbox("Uso", ["Personal", "Negocio"])
    notas = st.text_area("Notas (opcional)")
    guardar_cuenta = st.button("Guardar cuenta")

    if guardar_cuenta:
        if cuenta_existe(nombre):
            st.warning(f"⚠️ La cuenta '{nombre}' ya existe")
        else:
            ok = guardar_cuenta_db(nombre, tipo, saldo_inicial, moneda, uso, notas)
            if ok:
                st.success(f"✅ Cuenta '{nombre}' guardada en la base de datos")
                st.experimental_rerun()
            else:
                st.error("❌ No se pudo guardar la cuenta")

# --- SUBCATEGORÍAS ---
st.subheader("📂 Subcategorías registradas")
subcategorias = cargar_subcategorias_db()
df_sub = pd.DataFrame(subcategorias)
st.dataframe(df_sub, use_container_width=True)

with st.expander("➕ Agregar nueva subcategoría"):
    categoria = st.text_input("Categoría")
    subcategoria = st.text_input("Subcategoría")
    tipo = st.selectbox("Uso", ["Personal", "Negocio"])
    guardar_sub = st.button("Guardar subcategoría")

    if guardar_sub:
        if subcategoria_existe(categoria, subcategoria):
            st.warning(f"⚠️ La subcategoría '{subcategoria}' ya existe en '{categoria}'")
        else:
            ok = guardar_subcategoria_db(categoria, subcategoria, tipo)
            if ok:
                st.success(f"✅ Subcategoría '{subcategoria}' guardada bajo '{categoria}'")
                st.experimental_rerun()
            else:
                st.error("❌ No se pudo guardar la subcategoría")
