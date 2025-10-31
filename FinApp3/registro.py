import streamlit as st
import pandas as pd
from utils_db import cargar_subcategorias_db, guardar_transaccion_db, cargar_cuentas_db

st.set_page_config(page_title="Registro de transacciones", layout="wide")
st.title("🧾 Registro de transacciones")

# --- Paso 1: seleccionar uso ---
uso = st.selectbox("¿Esta transacción es Personal o de Negocio?", ["Personal", "Negocio"])

# --- Cargar subcategorías filtradas ---
subcategorias = cargar_subcategorias_db()
df_sub = pd.DataFrame(subcategorias)
df_filtradas = df_sub[df_sub["tipo"] == uso]

# --- Cargar cuentas filtradas ---
cuentas = cargar_cuentas_db()
df_cuentas = pd.DataFrame(cuentas)
cuentas_filtradas = df_cuentas[df_cuentas["uso"] == uso]["nombre"].tolist()

# --- Formulario principal ---
col1, col2 = st.columns(2)
with col1:
    fecha = st.date_input("Fecha")
    tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
    cuenta = st.selectbox("Cuenta", cuentas_filtradas)

with col2:
    categoria = st.selectbox("Categoría", sorted(df_filtradas["categoria"].unique()))
    subcat_opciones = df_filtradas[df_filtradas["categoria"] == categoria]["subcategoria"].tolist()
    subcategoria = st.selectbox("Subcategoría", subcat_opciones)

descripcion = st.text_input("Descripción")
monto = st.number_input("Monto", step=100.0)
guardar = st.button("Guardar transacción")

if guardar:
    ok = guardar_transaccion_db(fecha, tipo, cuenta, categoria, subcategoria, monto, descripcion, "", uso)
    if ok:
        st.success("✅ Transacción guardada correctamente")
    else:
        st.error("❌ No se pudo guardar la transacción")
