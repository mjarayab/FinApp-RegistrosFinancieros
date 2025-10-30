import sqlite3
import os

# Crear carpeta si no existe
os.makedirs("data", exist_ok=True)

# Conectar y crear base de datos
conn = sqlite3.connect("data/finapp.db")
cursor = conn.cursor()

# Tabla de transacciones
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

# Tabla de cuentas
cursor.execute("""
CREATE TABLE IF NOT EXISTS cuentas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    tipo TEXT,
    saldo_inicial REAL,
    moneda TEXT,
    uso TEXT,
    notas TEXT
)
""")

# Tabla de subcategorías
cursor.execute("""
CREATE TABLE IF NOT EXISTS subcategorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT,
    subcategoria TEXT,
    tipo TEXT
)
""")

conn.commit()
conn.close()
print("✅ Base de datos FinApp creada en data/finapp.db")
