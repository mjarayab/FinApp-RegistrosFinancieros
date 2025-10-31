import streamlit as st
import pandas as pd
from utils_db import cargar_transacciones_db, actualizar_transaccion_db

st.title("💰 FinApp - Panel de Transacciones")

# Cargar transacciones
transacciones = cargar_transacciones_db()

if not transacciones:
    st.warning("⚠️ No se cargaron transacciones desde la base de datos.")
else:
    df = pd.DataFrame(transacciones)
    df["fecha"] = pd.to_datetime(df["fecha"])

    st.success(f"✅ Se cargaron {len(df)} transacciones")

    # Filtros
    st.sidebar.header("🔍 Filtros")

    fecha_min = df["fecha"].min()
    fecha_max = df["fecha"].max()

    fecha_inicio = st.sidebar.date_input("Desde", fecha_min)
    fecha_fin = st.sidebar.date_input("Hasta", fecha_max)

    tipos = st.sidebar.multiselect("Tipo", options=df["tipo"].unique(), default=list(df["tipo"].unique()))
    cuentas = st.sidebar.multiselect("Cuenta", options=df["cuenta"].unique(), default=list(df["cuenta"].unique()))
    categorias = st.sidebar.multiselect("Categoría", options=df["categoria"].unique(), default=list(df["categoria"].unique()))

    # Aplicar filtros
    transacciones_filtradas = df[
        (df["fecha"] >= pd.to_datetime(fecha_inicio)) &
        (df["fecha"] <= pd.to_datetime(fecha_fin)) &
        (df["tipo"].isin(tipos)) &
        (df["cuenta"].isin(cuentas)) &
        (df["categoria"].isin(categorias))
    ].sort_values("fecha", ascending=False)

    st.subheader(f"📋 Transacciones filtradas ({len(transacciones_filtradas)})")
    st.dataframe(transacciones_filtradas, use_container_width=True)

    # Panel de edición
    st.subheader("✏️ Editar transacción")

    opciones = [
        f"{t['id']}: {t['descripcion']} ({t['fecha'].strftime('%d %b %Y')})"
        for _, t in transacciones_filtradas.iterrows()
    ]

    if opciones:
        seleccion = st.selectbox("Selecciona una transacción", opciones)
        transaccion_id = int(seleccion.split(":")[0])
        transaccion = transacciones_filtradas[transacciones_filtradas["id"] == transaccion_id].iloc[0]

        nueva_fecha = st.date_input("Fecha", transaccion["fecha"])
        nuevo_tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"], index=["Ingreso", "Gasto"].index(transaccion["tipo"]))
        nueva_cuenta = st.text_input("Cuenta", transaccion["cuenta"])
        nueva_categoria = st.text_input("Categoría", transaccion["categoria"])
        nueva_subcategoria = st.text_input("Subcategoría", transaccion["subcategoria"])
        nuevo_monto = st.number_input("Monto", value=transaccion["monto"], step=0.01)
        nueva_descripcion = st.text_input("Descripción", transaccion["descripcion"])
        nuevo_proyecto = st.text_input("Proyecto", transaccion["proyecto"])
        nuevo_uso = st.text_input("Uso", transaccion["uso"])

        if st.button("Guardar cambios"):
            actualizar_transaccion_db(
                transaccion_id,
                nueva_fecha.strftime("%Y-%m-%d"),
                nuevo_tipo,
                nueva_cuenta,
                nueva_categoria,
                nueva_subcategoria,
                nuevo_monto,
                nueva_descripcion,
                nuevo_proyecto,
                nuevo_uso
            )
            st.success("✅ Transacción actualizada correctamente")
    else:
        st.info("No hay transacciones que coincidan con los filtros.")
