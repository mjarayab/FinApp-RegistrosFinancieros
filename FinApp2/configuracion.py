import streamlit as st
import pandas as pd
from utils_db import cargar_cuentas_db, cargar_subcategorias_db  # ← cambio aquí

st.set_page_config(page_title="Configuración", layout="wide")
st.title("⚙️ Configuración de FinApp2")

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
        st.success(f"✅ Cuenta '{nombre}' registrada (simulado)")
        st.write({
            "nombre": nombre,
            "tipo": tipo,
            "saldo_inicial": saldo_inicial,
            "moneda": moneda,
            "uso": uso,
            "notas": notas
        })

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
        st.success(f"✅ Subcategoría '{subcategoria}' registrada bajo '{categoria}' (simulado)")
        st.write({
            "categoria": categoria,
            "subcategoria": subcategoria,
            "tipo": tipo
        })
