import streamlit as st
import pandas as pd
import plotly.express as px
from utils_db import cargar_transacciones_db, actualizar_transaccion_db

st.set_page_config(page_title="FinApp", layout="wide")
st.title("💰 FinApp - Panel de Transacciones")

# Cargar datos
transacciones = cargar_transacciones_db()
if not transacciones:
    st.warning("⚠️ No se cargaron transacciones desde la base de datos.")
    st.stop()

df = pd.DataFrame(transacciones)
df["fecha"] = pd.to_datetime(df["fecha"])

# Filtros
st.sidebar.header("🔍 Filtros")

fecha_inicio = st.sidebar.date_input("Desde", df["fecha"].min())
fecha_fin = st.sidebar.date_input("Hasta", df["fecha"].max())

tipo = st.sidebar.selectbox("Tipo", ["Todos"] + sorted(df["tipo"].unique()))
cuenta = st.sidebar.selectbox("Cuenta", ["Todas"] + sorted(df["cuenta"].unique()))
categoria = st.sidebar.selectbox("Categoría", ["Todas"] + sorted(df["categoria"].unique()))

# Aplicar filtros
filtradas = df[
    (df["fecha"] >= pd.to_datetime(fecha_inicio)) &
    (df["fecha"] <= pd.to_datetime(fecha_fin))
]

if tipo != "Todos":
    filtradas = filtradas[filtradas["tipo"] == tipo]
if cuenta != "Todas":
    filtradas = filtradas[filtradas["cuenta"] == cuenta]
if categoria != "Todas":
    filtradas = filtradas[filtradas["categoria"] == categoria]

# Tabla
st.subheader(f"📋 Transacciones filtradas ({len(filtradas)})")
st.dataframe(filtradas.sort_values("fecha", ascending=False), use_container_width=True, hide_index=True)

# Resumen por cuenta
st.subheader("📊 Resumen por cuenta")
resumen = filtradas.groupby(["cuenta", "tipo"])["monto"].sum().unstack(fill_value=0)
resumen["Balance"] = resumen.get("Ingreso", 0) - resumen.get("Gasto", 0)
st.dataframe(resumen, use_container_width=True)

# Gráfico de ingresos vs gastos
st.subheader("📈 Ingresos vs Gastos")
grafico = filtradas.groupby(["fecha", "tipo"])["monto"].sum().reset_index()
fig = px.bar(grafico, x="fecha", y="monto", color="tipo", barmode="group", title="Ingresos vs Gastos por fecha")
st.plotly_chart(fig, use_container_width=True)

# Panel de edición
st.subheader("✏️ Editar transacción")

opciones = [f"{row['id']}: {row['descripcion']} ({row['fecha'].strftime('%d %b %Y')})" for _, row in filtradas.iterrows()]
if opciones:
    seleccion = st.selectbox("Selecciona una transacción", opciones)
    transaccion_id = int(seleccion.split(":")[0])
    t = filtradas[filtradas["id"] == transaccion_id].iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        nueva_fecha = st.date_input("Fecha", t["fecha"])
        nuevo_tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"], index=["Ingreso", "Gasto"].index(t["tipo"]))
        nueva_cuenta = st.text_input("Cuenta", t["cuenta"])
        nueva_categoria = st.text_input("Categoría", t["categoria"])
        nueva_subcategoria = st.text_input("Subcategoría", t["subcategoria"])
    with col2:
        nuevo_monto = st.number_input("Monto", value=t["monto"], step=0.01)
        nueva_descripcion = st.text_input("Descripción", t["descripcion"])
        nuevo_proyecto = st.text_input("Proyecto", t["proyecto"])
        nuevo_uso = st.text_input("Uso", t["uso"])

    if st.button("Guardar cambios"):
        actualizar_transaccion_db(
            transaccion_id,
            nueva_fecha.strftime("%Y-%m-%d"),
            nuevo_tipo,
            nueva_cuenta,
            nueva_categoria,
            nueva_subcategoria,
            nuevo_monto,
            nueva_descripcion,
            nuevo_proyecto,
            nuevo_uso
        )
        st.success("✅ Transacción actualizada correctamente")
else:
    st.info("No hay transacciones que coincidan con los filtros.")
