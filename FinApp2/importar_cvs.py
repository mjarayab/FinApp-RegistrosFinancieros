import pandas as pd
import sqlite3

DB_PATH = "data/finapp.db"

# --- Cargar CSVs con encabezados reales ---
df_trans = pd.read_csv("data/transacciones.csv")
df_cuentas = pd.read_csv("data/cuentas.csv")
df_subs = pd.read_csv("data/subcategorias.csv")

# Conexión a SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# --- Migrar transacciones ---
for _, row in df_trans.iterrows():
    cursor.execute("""
        INSERT INTO transacciones (fecha, tipo, cuenta, categoria, subcategoria, monto, descripcion, proyecto, uso)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["Fecha"], row["Ingreso/Gasto"], row["Cuenta"], row["Categoría"], row["Subcategoría"],
        row["Monto"], row.get("Descripcion", ""), "", row["Personal_Negocio"]
    ))

# --- Migrar cuentas ---
for _, row in df_cuentas.iterrows():
    cursor.execute("SELECT COUNT(*) FROM cuentas WHERE nombre = ?", (row["Cuenta"],))
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO cuentas (nombre, tipo, saldo_inicial, moneda, uso, notas)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row["Cuenta"], row["Tipo"], row.get("Saldo Inicial", 0), row["Moneda"],
            row["Personal_Negocio"], ""
        ))

# --- Migrar subcategorías ---
for _, row in df_subs.iterrows():
    cursor.execute("""
        SELECT COUNT(*) FROM subcategorias
        WHERE categoria = ? AND subcategoria = ?
    """, (row["Categoría"], row["Subcategoría"]))
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO subcategorias (categoria, subcategoria, tipo)
            VALUES (?, ?, ?)
        """, (
            row["Categoría"], row["Subcategoría"], row["Personal/Negocio"]
        ))

conn.commit()
conn.close()
print("✅ Migración completada desde tus archivos CSV a finapp.db")
