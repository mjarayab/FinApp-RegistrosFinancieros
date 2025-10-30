import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils_db import cargar_transacciones_db, cargar_cuentas_db, cargar_subcategorias_db

st.set_page_config(page_title="FinApp2", layout="wide")
st.title("📊 Panel financiero")

# --- Cargar datos ---
df = cargar_transacciones_db()
df.columns = df.columns.str.strip().str.lower()
df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

# --- Panel de filtros ---
with st.sidebar:
    st.header("🎛️ Filtros")

    uso = st.selectbox("Tipo de uso", ["Todas", "Personal", "Negocio"], index=0)

    cuentas = cargar_cuentas_db()
    df_cuentas = pd.DataFrame(cuentas)
    cuentas_filtradas = df_cuentas["nombre"].tolist() if uso == "Todas" else df_cuentas[df_cuentas["uso"] == uso]["nombre"].tolist()
    cuenta = st.selectbox("Cuenta", ["Todas"] + cuentas_filtradas)

    subcats = cargar_subcategorias_db()
    df_sub = pd.DataFrame(subcats)
    df_sub = df_sub if uso == "Todas" else df_sub[df_sub["tipo"] == uso]

    categoria = st.selectbox("Categoría", ["Todas"] + sorted(df_sub["categoria"].unique()))
    subcat_opciones = df_sub[df_sub["categoria"] == categoria]["subcategoria"].tolist() if categoria != "Todas" else []
    subcategoria = st.selectbox("Subcategoría", ["Todas"] + subcat_opciones)

    fecha_inicio = st.date_input("Desde", value=df["fecha"].min())
    fecha_fin = st.date_input("Hasta", value=df["fecha"].max())

# --- Aplicar filtros ---
df_filtrado = df.copy()
df_filtrado = df_filtrado[(df_filtrado["fecha"] >= pd.to_datetime(fecha_inicio)) & (df_filtrado["fecha"] <= pd.to_datetime(fecha_fin))]

if uso != "Todas":
    df_filtrado = df_filtrado[df_filtrado["uso"] == uso]
if cuenta != "Todas":
    df_filtrado = df_filtrado[df_filtrado["cuenta"] == cuenta]
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria"] == categoria]
if subcategoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["subcategoria"] == subcategoria]

# --- Mostrar resultados ---
st.subheader("📄 Transacciones filtradas")
st.dataframe(df_filtrado, use_container_width=True)

# --- Gráfico con valores negativos ---
st.subheader("📈 Resumen por categoría (incluye negativos)")
if not df_filtrado.empty:
    resumen = df_filtrado.groupby("categoria")["monto"].sum().reset_index()
    fig, ax = plt.subplots()
    ax.bar(resumen["categoria"], resumen["monto"], color=["green" if x >= 0 else "red" for x in resumen["monto"]])
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_ylabel("Monto total")
    ax.set_xlabel("Categoría")
    ax.set_title("Resumen por categoría")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)
else:
    st.info("No hay transacciones que coincidan con los filtros seleccionados.")
