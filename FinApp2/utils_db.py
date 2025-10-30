import pandas as pd
import sqlite3
import streamlit as st

# --- TRANSACCIONES ---
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

# --- CUENTAS ---
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

def cuenta_existe(nombre):
    try:
        conn = sqlite3.connect("data/finapp.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cuentas WHERE nombre = ?", (nombre,))
        existe = cursor.fetchone()[0] > 0
        conn.close()
        return existe
    except Exception as e:
        st.error(f"Error al verificar cuenta: {e}")
        return False

def guardar_cuenta_db(nombre, tipo, saldo_inicial, moneda, uso, notas):
    try:
        conn = sqlite3.connect("data/finapp.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cuentas (nombre, tipo, saldo_inicial, moneda, uso, notas)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, tipo, saldo_inicial, moneda, uso, notas))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error al guardar cuenta: {e}")
        return False

# --- SUBCATEGORÍAS ---
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

def subcategoria_existe(categoria, subcategoria):
    try:
        conn = sqlite3.connect("data/finapp.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM subcategorias
            WHERE categoria = ? AND subcategoria = ?
        """, (categoria, subcategoria))
        existe = cursor.fetchone()[0] > 0
        conn.close()
        return existe
    except Exception as e:
        st.error(f"Error al verificar subcategoría: {e}")
        return False

def guardar_subcategoria_db(categoria, subcategoria, tipo):
    try:
        conn = sqlite3.connect("data/finapp.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO subcategorias (categoria, subcategoria, tipo)
            VALUES (?, ?, ?)
        """, (categoria, subcategoria, tipo))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error al guardar subcategoría: {e}")
        return False
