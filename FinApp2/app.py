import streamlit as st
import pandas as pd
from utils_db import cargar_transacciones_db, actualizar_transaccion_db

st.title("💰 FinApp - Panel de Transacciones")

# Cargar transacciones desde la base
transacciones = cargar_transacciones_db()

if not transacciones:
    st.warning("⚠️ No se cargaron transacciones desde la base de datos.")
else:
    st.success(f"✅ Se cargaron {len(transacciones)} transacciones")

    # Mostrar tabla completa
    df = pd.DataFrame(transacciones)
    df["fecha"] = pd.to_datetime(df["fecha"])
    st.dataframe(df.sort_values("fecha", ascending=False), use_container_width=True)

    # Panel de edición
    st.subheader("✏️ Editar transacción")

    # Opciones simplificadas
    opciones = [
        f"{t['id']}: {t['descripcion']} ({pd.to_datetime(t['fecha']).strftime('%d %b %Y')})"
        for t in transacciones
    ]

    seleccion = st.selectbox("Selecciona una transacción", opciones)

    if seleccion:
        transaccion_id = int(seleccion.split(":")[0])
        transaccion = next((t for t in transacciones if t["id"] == transaccion_id), None)

        if transaccion:
            # Formulario editable
            nueva_fecha = st.date_input("Fecha", pd.to_datetime(transaccion["fecha"]))
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
