import sqlite3
import pandas as pd

DB_PATH = "data/finapp.db"

# --- CUENTAS ---
def cargar_cuentas_db():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM cuentas", conn)
    conn.close()
    return df.to_dict(orient="records")

def cuenta_existe(nombre):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cuentas WHERE nombre = ?", (nombre,))
    existe = cursor.fetchone()[0] > 0
    conn.close()
    return existe

def guardar_cuenta_db(nombre, tipo, saldo_inicial, moneda, uso, notas):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cuentas (nombre, tipo, saldo_inicial, moneda, uso, notas)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, tipo, saldo_inicial, moneda, uso, notas))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error al guardar cuenta:", e)
        return False

# --- SUBCATEGORÍAS ---
def cargar_subcategorias_db():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM subcategorias", conn)
    conn.close()
    return df.to_dict(orient="records")

def subcategoria_existe(categoria, subcategoria):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM subcategorias
        WHERE categoria = ? AND subcategoria = ?
    """, (categoria, subcategoria))
    existe = cursor.fetchone()[0] > 0
    conn.close()
    return existe

def guardar_subcategoria_db(categoria, subcategoria, tipo):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO subcategorias (categoria, subcategoria, tipo)
            VALUES (?, ?, ?)
        """, (categoria, subcategoria, tipo))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error al guardar subcategoría:", e)
        return False

# --- TRANSACCIONES ---
def cargar_transacciones_db():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM transacciones", conn)
    conn.close()
    return df

def guardar_transaccion_db(fecha, tipo, cuenta, categoria, subcategoria, monto, descripcion, proyecto, uso):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transacciones (fecha, tipo, cuenta, categoria, subcategoria, monto, descripcion, proyecto, uso)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (fecha, tipo, cuenta, categoria, subcategoria, monto, descripcion, proyecto, uso))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error al guardar transacción:", e)
        return False
