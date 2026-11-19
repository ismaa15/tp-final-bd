## ENTREGA DE TRABAJO PRACTICO FINAL DE BASE DE DATOS ##
Requisitos previos para el funcionamiento del programa

de gestion de inventario programado en Python, con el motor 

de Base de Datos Sqlite3 y una interfaz grafica impulsado

por Customtkinter (libreria externa basada en Tkinter)

## Comandos para la instalacion de Customtkinter:
**REQUIERE PYTHON 3.7 O SUPERIOR** (Documentacion Oficial de Customtkinter)

pip3 install customtkinter (Terminal de Powershell o MacOs)

sudo apt install python3-tk (Linux)

## En caso de no tener instalado Python
```winget install Python (Terminal de Powershell)```

```[Python.org](https://www.python.org/downloads/) para cualquier sistema operativo```

```python --version (Para verificar que fue instalado) ```

>## **IMPORTANTE**
En caso de que, al momento de ejecutar este proyecto exista el archivo <br>
`inventario.db` eliminarlo, este mismo se genera automaticamente al <br>
correr el programa
>## **IMPORTANTE**
En caso de que, al momento de ejecutar este proyecto exista el archivo <br>
`inventario.db` eliminarlo, este mismo se genera automaticamente al <br>
correr el programa

## Como ejecutar el programa
Ctrl + Alt + N en archivo main.py<br>
Desde terminal moverse hasta la ruta de acceso y correr el siguiente comando:<br>
`python main.py`

## Creacion de proyecto y carpetas moduladas dentro de IDE
```
├── main.py            # punto de entrada: crea la ventana y arranca la app
├── db.py              # conexión y funciones SQL CRUD
├── ui/
│   ├── ventana_producto.py # Crea la interfaz grafica de productos
│   └── ventana_categoria.py # Crea la interfaz grafica de categorias y proveedores
├── sql/
│   ├── esquema.sql    # Creacion de las tablas con sus respectivas caracteristicas
│   └── datos.sql      # Inserta datos de los productos
│   └── consultas.sql  # 
├── inventario.db      
└── README.md          # Explicacion paso a paso del proyecto para ejecutar e instalar
```
