import sqlite3
import os

DB_PATH = "data/finapp.db"

def conectar_db():
    """Establece conexión con la base de datos."""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"No se encontró la base de datos en {DB_PATH}")
    return sqlite3.connect(DB_PATH)

def cargar_transacciones_db():
    """Carga todas las transacciones como lista de diccionarios."""
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transacciones")
        columnas = [col[0] for col in cursor.description]
        datos = cursor.fetchall()
        conn.close()
        return [dict(zip(columnas, fila)) for fila in datos]
    except Exception as e:
        print("❌ Error al cargar transacciones:", e)
        return []

def actualizar_transaccion_db(id, fecha, tipo, cuenta, categoria, subcategoria, monto, descripcion, proyecto, uso):
    """Actualiza una transacción existente por ID."""
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE transacciones
            SET fecha = ?, tipo = ?, cuenta = ?, categoria = ?, subcategoria = ?, monto = ?, descripcion = ?, proyecto = ?, uso = ?
            WHERE id = ?
        """, (fecha, tipo, cuenta, categoria, subcategoria, monto, descripcion, proyecto, uso, id))
        conn.commit()
        conn.close()
        print(f"✅ Transacción {id} actualizada")
    except Exception as e:
        print(f"❌ Error al actualizar transacción {id}:", e)

# Funciones adicionales que podrías agregar:
# - insertar_transaccion_db()
# - eliminar_transaccion_db()
# - cargar_cuentas_db()
# - cargar_subcategorias_db()

def cargar_subcategorias_db():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT subcategoria FROM transacciones ORDER BY subcategoria")
        subcategorias = [row[0] for row in cursor.fetchall()]
        conn.close()
        return subcategorias
    except Exception as e:
        print("❌ Error al cargar subcategorías:", e)
        return []

def cargar_cuentas_db():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT cuenta FROM transacciones ORDER BY cuenta")
        cuentas = [row[0] for row in cursor.fetchall()]
        conn.close()
        return cuentas
    except Exception as e:
        print("❌ Error al cargar cuentas:", e)
        return []

def guardar_transaccion_db(fecha, tipo, cuenta, categoria, subcategoria, monto, descripcion, proyecto, uso):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transacciones (fecha, tipo, cuenta, categoria, subcategoria, monto, descripcion, proyecto, uso)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (fecha, tipo, cuenta, categoria, subcategoria, monto, descripcion, proyecto, uso))
        conn.commit()
        conn.close()
        print("✅ Transacción guardada correctamente")
    except Exception as e:
        print("❌ Error al guardar transacción:", e)
