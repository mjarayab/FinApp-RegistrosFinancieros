st.subheader("✏️ Editar transacción")

opciones = [f"{row['id']}: {row['descripcion']} ({row['fecha'].strftime('%d %b %Y')})" for _, row in filtradas.iterrows()]
if opciones:
    seleccion = st.selectbox("Selecciona una transacción", opciones)
    transaccion_id = int(seleccion.split(":")[0])
    t = filtradas[filtradas["id"] == transaccion_id].iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        nueva_fecha = st.date_input("Fecha", t["fecha"])
        nuevo_tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"], index=["Ingreso", "Gasto"].index(t["tipo"]))
        nueva_cuenta = st.text_input("Cuenta", t["cuenta"])
        nueva_categoria = st.text_input("Categoría", t["categoria"])
        nueva_subcategoria = st.text_input("Subcategoría", t["subcategoria"])
    with col2:
        nuevo_monto = st.number_input("Monto", value=t["monto"], step=0.01)
        nueva_descripcion = st.text_input("Descripción", t["descripcion"])
        nuevo_proyecto = st.text_input("Proyecto", t["proyecto"])
        nuevo_uso = st.text_input("Uso", t["uso"])

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

    if st.button("🗑️ Eliminar transacción"):
        import sqlite3
        conn = sqlite3.connect("data/finapp.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transacciones WHERE id = ?", (transaccion_id,))
        conn.commit()
        conn.close()
        st.success(f"✅ Transacción {transaccion_id} eliminada correctamente")
else:
    st.info("No hay transacciones que coincidan con los filtros.")
