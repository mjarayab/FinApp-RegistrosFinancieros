FinApp
======

FinApp es una aplicación web desarrollada con Python y Streamlit para el 
registro y seguimiento de transacciones financieras. Está diseñada con una 
arquitectura modular que permite escalar el sistema para incluir 
funcionalidades como inventario, cotizaciones, reportes y más.

---

🚀 Características principales

- Registro de transacciones con validación dinámica de categorías y 
subcategorías.
- Campos personalizables como cuenta, proyecto, monto y fecha.
- Interfaz web intuitiva construida con Streamlit.
- Preparada para expansión modular (inventario, cotizaciones, reportes).
- Base de datos local con SQLite (opcionalmente escalable a PostgreSQL).

---

🧱 Estructura del proyecto

FinApp/
├── app.py                 # Archivo principal de la aplicación 
Streamlit
├── venv/                  # Entorno virtual (excluido del repositorio)
├── data/                  # Carpeta para la base de datos SQLite
│   └── transactions.db
├── modules/               # Carpeta para módulos futuros
│   ├── inventario/
│   ├── cotizaciones/
│   └── reportes/
├── .gitignore             # Exclusión de archivos innecesarios
├── README.txt             # Documentación del proyecto

---

⚙️ Instalación y ejecución

1. Clonar el repositorio:
   git clone https://github.com/tuusuario/FinApp.git
   cd FinApp

2. Crear y activar el entorno virtual:
   python3 -m venv venv
   source venv/bin/activate

3. Instalar dependencias:
   pip install -r requirements.txt

4. Ejecutar la aplicación:
   streamlit run app.py

---

🗃️ Esquema de base de datos (SQLite)

CREATE TABLE categorias (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE subcategorias (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    categoria_id INTEGER,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE transacciones (
    id INTEGER PRIMARY KEY,
    fecha TEXT,
    monto REAL,
    categoria_id INTEGER,
    subcategoria_id INTEGER,
    cuenta TEXT,
    proyecto TEXT,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id),
    FOREIGN KEY (subcategoria_id) REFERENCES subcategorias(id)
);

---

📦 Módulos futuros

- Inventario: gestión de productos, existencias y proveedores.
- Cotizaciones: generación y seguimiento de presupuestos para clientes.
- Reportes: visualización de métricas financieras y exportación de datos.

---

☁️ Opciones de despliegue

- Red local: accesible desde dispositivos móviles en la misma red.
- Streamlit Cloud: hosting gratuito para prototipos.
- Render / Fly.io / Heroku: opciones escalables para producción.

---

🧠 Autor

Mauricio Araya 

