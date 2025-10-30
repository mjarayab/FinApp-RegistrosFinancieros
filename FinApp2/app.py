import streamlit as st
import pandas as pd
from utils import cargar_transacciones, cargar_subcategorias, cargar_cuentas

st.set_page_config(page_title="FinApp2", layout="wide")
st.title("📊 FinApp2 — Finanzas Personales y de Negocio")

# Cargar datos
transacciones = cargar_transacciones()
subcategorias = cargar_subcategorias()
cuentas = cargar_cuentas()

if transacciones.empty:
    st.warning("No se pudieron cargar las transacciones.")
    st.stop()

# Filtros
with st.sidebar:
    st.header("🔍 Filtros")

    cuentas_disponibles = sorted(transacciones["Cuenta"].dropna().unique())
    cuenta_seleccionada = st.multiselect("Cuenta", cuentas_disponibles, default=cuentas_disponibles)

    tipos_disponibles = sorted(transacciones["Tipo"].dropna().unique())
    tipo_seleccionado = st.multiselect("Tipo", tipos_disponibles, default=tipos_disponibles)

    categorias_disponibles = sorted(transacciones["Categoría"].dropna().unique())
    categoria_seleccionada = st.multiselect("Categoría", categorias_disponibles, default=categorias_disponibles)

    fecha_min = transacciones["Fecha"].min()
    fecha_max = transacciones["Fecha"].max()
    rango_fechas = st.date_input("Rango de fechas", [fecha_min, fecha_max])

# Aplicar filtros
filtro = (
    transacciones["Cuenta"].isin(cuenta_seleccionada) &
    transacciones["Tipo"].isin(tipo_seleccionado) &
    transacciones["Categoría"].isin(categoria_seleccionada) &
    (transacciones["Fecha"] >= pd.to_datetime(rango_fechas[0])) &
    (transacciones["Fecha"] <= pd.to_datetime(rango_fechas[1]))
)

transacciones_filtradas = transacciones[filtro]

# Mostrar tabla
st.subheader("📋 Transacciones filtradas")
st.dataframe(transacciones_filtradas.sort_values("Fecha", ascending=False), use_container_width=True)

# Totales
total_gastos = transacciones_filtradas[transacciones_filtradas["Tipo"] == "Gasto"]["Monto"].sum()
total_ingresos = transacciones_filtradas[transacciones_filtradas["Tipo"] == "Ingreso"]["Monto"].sum()
balance = total_ingresos - total_gastos

st.markdown(f"""
### 💰 Resumen
- **Total ingresos:** ₡{total_ingresos:,.0f}
- **Total gastos:** ₡{total_gastos:,.0f}
- **Balance neto:** ₡{balance:,.0f}
""")
