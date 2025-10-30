import streamlit as st
import pandas as pd
from utils import cargar_subcategorias, cargar_cuentas

st.set_page_config(page_title="Registro", layout="wide")
st.title("📝 Registro de Transacciones")

subcategorias = cargar_subcategorias()
cuentas = cargar_cuentas()

# Extraer listas únicas
lista_cuentas = [c["nombre"] for c in cuentas]
lista_categorias = sorted(set([s["categoria"] for s in subcategorias]))
lista_subcategorias = sorted(set([s["subcategoria"] for s in subcategorias]))
lista_tipos = ["Ingreso", "Gasto"]
lista_uso = ["Personal", "Negocio"]

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
        nueva = {
            "Fecha": pd.to_datetime(fecha),
            "Tipo": tipo,
            "Cuenta": cuenta,
            "Categoría": categoria,
            "Subcategoría": subcategoria,
            "Monto": monto,
            "Descripción": descripcion,
            "Proyecto": proyecto,
            "Personal_Negocio": uso
        }

        st.success("✅ Transacción registrada")
        st.dataframe(pd.DataFrame([nueva]))
