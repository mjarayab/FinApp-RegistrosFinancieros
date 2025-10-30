import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import cargar_transacciones

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📈 Dashboard Financiero")

df = cargar_transacciones()
if df.empty:
    st.warning("No hay datos para mostrar.")
    st.stop()

# Filtrar solo gastos
df_gastos = df[df["Tipo"] == "Gasto"]

# Agrupar por categoría
gastos_por_categoria = df_gastos.groupby("Categoría")["Monto"].sum().sort_values(ascending=False)

# Gráfico de barras
st.subheader("💸 Gastos por Categoría")
fig, ax = plt.subplots(figsize=(10, 6))
colors = plt.cm.Set2.colors
bars = ax.bar(gastos_por_categoria.index, gastos_por_categoria.values, color=colors)
ax.set_ylabel("Monto (CRC)")
ax.set_xlabel("Categoría")
ax.set_title("Total de Gastos por Categoría")
ax.tick_params(axis='x', rotation=15)
ax.bar_label(bars, fmt='%.0f', padding=3)
st.pyplot(fig)
