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

# --- Resumen por categoría ---
st.subheader("📋 Resumen por categoría")
if not df_filtrado.empty:
    resumen = df_filtrado.groupby("categoria")["monto"].sum().reset_index()
    st.dataframe(resumen, use_container_width=True)

    # --- Gráfico de barras por categoría ---
    st.subheader("📈 Gráfico de montos por categoría")
    fig, ax = plt.subplots()
    ax.bar(resumen["categoria"], resumen["monto"], color=["green" if x >= 0 else "red" for x in resumen["monto"]])
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_ylabel("Monto total")
    ax.set_xlabel("Categoría")
    ax.set_title("Montos por categoría")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)
else:
    st.info("No hay transacciones que coincidan con los filtros seleccionados.")

# --- Resumen por cuenta y tipo ---
st.subheader("🏦 Resumen por cuenta y tipo de transacción")
if not df_filtrado.empty:
    resumen_cuentas = df_filtrado.groupby(["cuenta", "tipo"])["monto"].sum().unstack(fill_value=0)
    resumen_cuentas["balance"] = resumen_cuentas.get("ingreso", 0) - resumen_cuentas.get("gasto", 0)
    st.dataframe(resumen_cuentas, use_container_width=True)

    # --- Gráfico de ingresos y gastos por cuenta ---
    fig2, ax2 = plt.subplots()
    cuentas = resumen_cuentas.index.tolist()
    ingresos = resumen_cuentas.get("ingreso", pd.Series([0]*len(cuentas)))
    gastos = resumen_cuentas.get("gasto", pd.Series([0]*len(cuentas)))

    ax2.bar(cuentas, ingresos, label="Ingreso", color="green")
    ax2.bar(cuentas, -gastos, label="Gasto", color="red")
    ax2.axhline(0, color="gray", linewidth=0.8)
    ax2.set_ylabel("Monto")
    ax2.set_title("Ingresos y gastos por cuenta")
    ax2.legend()
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig2)
else:
    st.info("No hay transacciones para mostrar resumen por cuenta.")
