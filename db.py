import sqlite3
import os

def conectar():
    con = sqlite3.connect("inventario.db")
    con.execute("PRAGMA foreign_keys = ON")  # Habilitar claves foráneas

    return con

def inicializar_base():
    # Verifica si el archivo ya existe para no sobreescribir los datos cada vez que abres el programa
    if not os.path.exists("inventario.db"):
        with conectar() as con:
            # 1. Crea las tablas ejecutando el esquema[cite: 6]
            with open("sql/esquema.sql", "r", encoding="utf-8") as f:
                con.executescript(f.read())
            
            # 2. Inserta los datos obligatorios de prueba[cite: 6]
            with open("sql/datos.sql", "r", encoding="utf-8") as f:
                con.executescript(f.read())
        print("Base de datos creada y datos cargados con éxito.")

# Funciones de lectura para cargar los Combobox de tu interfaz gráfica
def listar_categorias():
    with conectar() as con:
        return con.execute("SELECT id_categoria, nombre FROM categorias ORDER BY nombre").fetchall()

def listar_proveedores():
    with conectar() as con:
        return con.execute("SELECT id_proveedor, razon_social FROM proveedores ORDER BY razon_social").fetchall()