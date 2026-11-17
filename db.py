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
        return con.execute("SELECT id_proveedor, cuit, razon_social, telefono, email FROM proveedores ORDER BY razon_social").fetchall()

def listar_productos():
    with conectar() as con:
        return con.execute (""""
        SELECT p.id_producto,
          p.codigo,
          p.nombre,
          c.nombre
          pr.razon_social,
          p.precio,
          p.stock,
          p.stock_minimo,
          p.descripcion
        FROM productos p
        INNER JOIN categorias c ON p.id_categoria = c.id_categoria
        INNER JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.codigo
        """).fetchall()

def insertar_producto(codigo, nombre, precio, stock, stock_minimo, id_categoria, id_proveedor):
    with conectar() as con:
        con.execute (
            """INSERT INTO productos
            (codigo, nombre, precio, stock, stock_minimo, id_categoria, id_proveedor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
          (codigo, nombre, precio, stock, stock_minimo, id_categoria, id_proveedor)
        )

def eliminar_producto(id_producto):
    with conectar() as con:
        con.execute(
            """DELETE FROM productos
            WHERE id_producto = (?)
            """,
            (id_producto,)
        )

def actualizar_producto(codigo, nombre, descripcion, precio, stock, stock_minimo, id_categoria, id_proveedor, id_producto):
    with conectar() as con:
        con.execute(
            """UPDATE productos
            SET codigo = ?, nombre = ?, descripcion = ?, precio = ?, stock = ?, stock_minimo = ?, id_categoria = ?, id_proveedor = ?
            WHERE id_producto = ?""",
        (codigo, nombre, descripcion, precio, stock, stock_minimo, id_categoria, id_proveedor, id_producto)
        )

def buscar_productos(texto):
    with conectar() as con:
        return con.execute(
            """SELECT p.id_producto, 
                      p.codigo, 
                      p.nombre, 
                      c.nombre, 
                      pr.razon_social,
                      p.precio, 
                      p.stock, 
                      p.stock_minimo,
                      p.descripcion
               FROM productos p 
               INNER JOIN categorias c ON p.id_categoria = c.id_categoria
               INNER JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
               WHERE p.codigo LIKE ? OR p.nombre LIKE ?
               ORDER BY p.codigo""",
            (f"%{texto}%", f"%{texto}%")
        ).fetchall()

def insertar_categoria(nombre):
    with conectar() as con:
        con.execute(
            """INSERT INTO categorias
            (nombre)
            VALUES (?)""",
            (nombre,)
        )

def eliminar_categoria(id_categoria):
    with conectar() as con:
        con.execute(
            """DELETE FROM categorias
            WHERE id_categoria = (?)
            """,
            (id_categoria,)
        )

def insertar_proveedor(cuit, razon_social, telefono, email):
    with conectar() as con:
        con.execute(
            """INSERT INTO proveedores
            (cuit, razon_social, telefono, email)
            VALUES (?, ?, ?, ?)""",
            (cuit, razon_social, telefono, email)
        )

def eliminar_proveedor(id_proveedor):
    with conectar() as con:
        con.execute(
            """DELETE FROM proveedores
            WHERE id_proveedor = ?
            """,
            (id_proveedor,)
        )
