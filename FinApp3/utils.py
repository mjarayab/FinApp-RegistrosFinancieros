import pandas as pd
import streamlit as st
import os

@st.cache_data
def cargar_transacciones():
    ruta = "data/transacciones.csv"
    if not os.path.exists(ruta):
        st.error(f"⚠️ No se encontró el archivo: {ruta}")
        return pd.DataFrame()

    df = pd.read_csv(ruta)

    df = df.rename(columns={
        "Ingreso/Gasto": "Tipo",
        "Subcategoria": "Subcategoría",
        "Categoria": "Categoría",
        "Cuenta": "Cuenta",
        "Monto": "Monto",
        "Fecha": "Fecha",
        "Descripcion": "Descripción",
        "Personal_Negocio": "Personal_Negocio"
    })

    if "Proyecto" not in df.columns:
        df["Proyecto"] = ""

    df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce")
    df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True)

    return df

@st.cache_data
def cargar_subcategorias():
    ruta = "data/subcategorias.csv"
    if not os.path.exists(ruta):
        st.error(f"⚠️ No se encontró el archivo: {ruta}")
        return []

    df = pd.read_csv(ruta)
    subcategorias = []
    for _, row in df.iterrows():
        subcategorias.append({
            "categoria": row["Categoría"],
            "subcategoria": row["Subcategoría"],
            "tipo": row["Personal/Negocio"]
        })
    return subcategorias

@st.cache_data
def cargar_cuentas():
    ruta = "data/cuentas.csv"
    if not os.path.exists(ruta):
        st.error(f"⚠️ No se encontró el archivo: {ruta}")
        return []

    df = pd.read_csv(ruta)
    cuentas = []
    for _, row in df.iterrows():
        cuentas.append({
            "nombre": row["Cuenta"],
            "tipo": row["Tipo"],
            "saldo_inicial": row["Saldo Inicial"],
            "moneda": row["Moneda"],
            "uso": row["Personal_Negocio"],
            "notas": row.get("Notas", "")
        })
    return cuentas
