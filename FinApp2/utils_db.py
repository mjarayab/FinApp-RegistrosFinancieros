import pandas as pd
import sqlite3
import streamlit as st

@st.cache_data
def cargar_transacciones_db():
    try:
        conn = sqlite3.connect("data/finapp.db")
        query = "SELECT * FROM transacciones"
        df = pd.read_sql_query(query, conn)
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
        st.error(f"Error al cargar desde la base de datos: {e}")
        return pd.DataFrame()
