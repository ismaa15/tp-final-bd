PRAGMA foreign_keys = ON;

create table categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

create table proveedores (
    id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT, 
    cuit VARCHAR(11) NOT NULL UNIQUE,
    razon_social VARCHAR(50) NOT NULL UNIQUE,
    telefono VARCHAR(15), 
    email VARCHAR(100)
);

create table productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT, 
    nombre VARCHAR(50) NOT NULL UNIQUE,
    codigo VARCHAR(10) NOT NULL, 
    descripcion VARCHAR(200), 
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    stock INTEGER NOT NULL CHECK (stock >= 0),
    stock_minimo INTEGER NOT NULL DEFAULT 0, 
    id_categoria INTEGER NOT NULL,
    id_proveedor INTEGER NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE RESTRICT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE RESTRICT
);
