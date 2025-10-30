import pandas as pd
import sqlite3
import streamlit as st

@st.cache_data
def cargar_transacciones_db():
    try:
        conn = sqlite3.connect("data/finapp.db")
        df = pd.read_sql_query("SELECT * FROM transacciones", conn)
        conn.close()

        df["Fecha"] = pd.to_datetime(df["fecha"])
        df["Monto"] = pd.to_numeric(df["monto"], errors="coerce")

        df = df.rename(columns={
            "tipo": "Tipo",
            "cuenta": "Cuenta",
            "categoria": "Categoría",
            "subcategoria": "Subcategoría",
            "descripcion": "Descripción",
            "proyecto": "Proyecto",
            "uso": "Personal_Negocio"
        })

        return df
    except Exception as e:
        st.error(f"Error al cargar transacciones: {e}")
        return pd.DataFrame()

@st.cache_data
def cargar_cuentas_db():
    try:
        conn = sqlite3.connect("data/finapp.db")
        df = pd.read_sql_query("SELECT * FROM cuentas", conn)
        conn.close()

        cuentas = []
        for _, row in df.iterrows():
            cuentas.append({
                "nombre": row["nombre"],
                "tipo": row["tipo"],
                "saldo_inicial": row["saldo_inicial"],
                "moneda": row["moneda"],
                "uso": row["uso"],
                "notas": row.get("notas", "")
            })
        return cuentas
    except Exception as e:
        st.error(f"Error al cargar cuentas: {e}")
        return []

@st.cache_data
def cargar_subcategorias_db():
    try:
        conn = sqlite3.connect("data/finapp.db")
        df = pd.read_sql_query("SELECT * FROM subcategorias", conn)
        conn.close()

        subcategorias = []
        for _, row in df.iterrows():
            subcategorias.append({
                "categoria": row["categoria"],
                "subcategoria": row["subcategoria"],
                "tipo": row["tipo"]
            })
        return subcategorias
    except Exception as e:
        st.error(f"Error al cargar subcategorías: {e}")
        return []
