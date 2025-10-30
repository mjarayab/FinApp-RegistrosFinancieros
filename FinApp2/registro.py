import streamlit as st
import pandas as pd
import sqlite3
from utils import cargar_subcategorias, cargar_cuentas

st.set_page_config(page_title="Registro", layout="wide")
st.title("📝 Registro de Transacciones")

# Cargar listas
subcategorias = cargar_subcategorias()
cuentas = cargar_cuentas()

lista_cuentas = [c["nombre"] for c in cuentas]
lista_categorias = sorted(set([s["categoria"] for s in subcategorias]))
lista_subcategorias = sorted(set([s["subcategoria"] for s in subcategorias]))
lista_tipos = ["Ingreso", "Gasto"]
lista_uso = ["Personal", "Negocio"]

# Conexión a SQLite
def conectar_db():
    conn = sqlite3.connect("data/finapp.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            tipo TEXT,
            cuenta TEXT,
            categoria TEXT,
            subcategoria TEXT,
            monto REAL,
            descripcion TEXT,
            proyecto TEXT,
            uso TEXT
        )
    """)
    conn.commit()
    return conn

with st.form("formulario_transaccion"):
    st.subheader("➕ Nueva transacción")

    fecha = st.date_input("Fecha")
    tipo = st.selectbox("Tipo", lista_tipos)
    cuenta = st.selectbox("Cuenta", lista_cuentas)
    categoria = st.selectbox("Categoría", lista_categorias)
    subcategoria = st.selectbox("Subcategoría", lista_subcategorias)
    monto = st.number_input("Monto", min_value=0.0, step=100.0)
    descripcion = st.text_input("Descripción")
    proyecto = st.text_input("Proyecto (opcional)")
    uso = st.selectbox("Personal o Negocio", lista_uso)

    submitted = st.form_submit_button("Guardar")

    if submitted:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transacciones (fecha, tipo, cuenta, categoria, subcategoria, monto, descripcion, proyecto, uso)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fecha.strftime("%Y-%m-%d"), tipo, cuenta, categoria, subcategoria,
            monto, descripcion, proyecto, uso
        ))
        conn.commit()
        conn.close()

        st.success("✅ Transacción guardada en la base de datos")
        st.dataframe(pd.DataFrame([{
            "Fecha": fecha,
            "Tipo": tipo,
            "Cuenta": cuenta,
            "Categoría": categoria,
            "Subcategoría": subcategoria,
            "Monto": monto,
            "Descripción": descripcion,
            "Proyecto": proyecto,
            "Uso": uso
        }]))
