import streamlit as st
import pandas as pd
from utils_db import cargar_transacciones_db, cargar_cuentas_db, cargar_subcategorias_db

st.set_page_config(page_title="FinApp2", layout="wide")
st.title("📊 Panel financiero")

# --- Cargar datos ---
df = cargar_transacciones_db()
df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

# --- Panel de filtros estilo Quicken ---
with st.sidebar:
    st.header("🎛️ Filtros")

    uso = st.selectbox("Tipo de uso", ["Personal", "Negocio"], index=0)

    cuentas = cargar_cuentas_db()
    cuentas_filtradas = [c["nombre"] for c in cuentas if c["uso"] == uso]
    cuenta = st.selectbox("Cuenta", ["Todas"] + cuentas_filtradas)

    subcats = cargar_subcategorias_db()
    df_sub = pd.DataFrame(subcats)
    df_sub = df_sub[df_sub["tipo"] == uso]

    categoria = st.selectbox("Categoría", ["Todas"] + sorted(df_sub["categoria"].unique()))
    subcat_opciones = df_sub[df_sub["categoria"] == categoria]["subcategoria"].tolist() if categoria != "Todas" else []
    subcategoria = st.selectbox("Subcategoría", ["Todas"] + subcat_opciones)

    fecha_inicio = st.date_input("Desde", value=df["Fecha"].min())
    fecha_fin = st.date_input("Hasta", value=df["Fecha"].max())

# --- Aplicar filtros ---
df_filtrado = df[df["uso"] == uso]
df_filtrado = df_filtrado[(df_filtrado["Fecha"] >= pd.to_datetime(fecha_inicio)) & (df_filtrado["Fecha"] <= pd.to_datetime(fecha_fin))]

if cuenta != "Todas":
    df_filtrado = df_filtrado[df_filtrado["cuenta"] == cuenta]
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria"] == categoria]
if subcategoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["subcategoria"] == subcategoria]

# --- Mostrar resultados ---
st.subheader("📄 Transacciones filtradas")
st.dataframe(df_filtrado, use_container_width=True)

st.subheader("📈 Resumen por categoría")
resumen = df_filtrado.groupby("categoria")["monto"].sum().reset_index()
st.bar_chart(resumen.set_index("categoria"))
