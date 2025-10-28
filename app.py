import streamlit as st
import pandas as pd
from datetime import date

# Cargar subcategorías desde CSV
@st.cache_data
def cargar_subcategorias():
    df = pd.read_csv("subcategorias.csv")
    estructura = {}
    for _, row in df.iterrows():
        cat = row["Categoría"]
        sub = row["Subcategoría"]
        tipo = row["Tipo"]
        if cat not in estructura:
            estructura[cat] = {}
        estructura[cat][sub] = tipo
    return estructura

SUBCATEGORIAS = cargar_subcategorias()

# Inicializar sesión
if "transacciones" not in st.session_state:
    st.session_state.transacciones = []

# Menú lateral
st.sidebar.title("📂 Menú")
opcion = st.sidebar.radio("Ir a:", ["Registro", "Dashboard", "Presupuesto"])

st.set_page_config(page_title="FinApp", layout="centered")

# Registro
if opcion == "Registro":
    st.title("📝 Registro de Transacciones")

    with st.form("form_transaccion"):
        fecha = st.date_input("Fecha", value=date.today())
        monto = st.number_input("Monto", min_value=0.0, format="%.2f")
        categoria = st.selectbox("Categoría", list(SUBCATEGORIAS.keys()))
        subcategoria = st.selectbox("Subcategoría", list(SUBCATEGORIAS[categoria].keys()))
        tipo = SUBCATEGORIAS[categoria][subcategoria]
        cuenta = st.text_input("Cuenta")
        proyecto = st.text_input("Proyecto")

        submitted = st.form_submit_button("Registrar")

        if submitted:
            nueva = {
                "Fecha": fecha,
                "Monto": monto,
                "Categoría": categoria,
                "Subcategoría": subcategoria,
                "Tipo": tipo,
                "Cuenta": cuenta,
                "Proyecto": proyecto
            }
            st.session_state.transacciones.append(nueva)
            st.success("✅ Transacción registrada correctamente.")

# Dashboard
elif opcion == "Dashboard":
    st.title("📊 Dashboard")
    if st.session_state.transacciones:
        df = pd.DataFrame(st.session_state.transacciones)
        resumen = df.groupby("Categoría")["Monto"].sum().reset_index()
        st.subheader("Total por categoría")
        st.dataframe(resumen)
    else:
        st.info("Aún no hay transacciones registradas.")

# Presupuesto
elif opcion == "Presupuesto":
    st.title("💰 Presupuesto")
    st.info("Aquí podrás definir y visualizar tu presupuesto por categoría. Próximamente.")
