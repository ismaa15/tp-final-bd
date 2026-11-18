import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3
import db


class FrameProductos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # Guarda el ID del producto seleccionado en la tabla (None si estamos creando uno nuevo)
        self.id_seleccionado = None
        self.mapa_categorias = {}
        self.mapa_proveedores = {}

        # Diseño de 1 fila y 2 columnas (columna 0: formulario, columna 1: tabla)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_formulario()
        self.crear_tabla()
        self.cargar_combos()
        self.refrescar_tabla()

    def crear_formulario(self):
        self.frame_form = ctk.CTkScrollableFrame(self, width=320)
        self.frame_form.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ns")

        ctk.CTkLabel(
            self.frame_form, text="Datos del Producto", font=("Arial", 16, "bold")
        ).pack(pady=(5, 10))

        # Código
        ctk.CTkLabel(self.frame_form, text="Código (ej. P009):").pack(anchor="w", padx=10)
        self.entry_codigo = ctk.CTkEntry(self.frame_form)
        self.entry_codigo.pack(fill="x", padx=10, pady=(0, 8))

        # Nombre
        ctk.CTkLabel(self.frame_form, text="Nombre:").pack(anchor="w", padx=10)
        self.entry_nombre = ctk.CTkEntry(self.frame_form)
        self.entry_nombre.pack(fill="x", padx=10, pady=(0, 8))

        # Descripción
        ctk.CTkLabel(self.frame_form, text="Descripción (opcional):").pack(anchor="w", padx=10)
        self.entry_descripcion = ctk.CTkEntry(self.frame_form)
        self.entry_descripcion.pack(fill="x", padx=10, pady=(0, 8))

        # Categoría (ComboBox)
        ctk.CTkLabel(self.frame_form, text="Categoría:").pack(anchor="w", padx=10)
        self.combo_cat = ctk.CTkComboBox(self.frame_form, state="readonly", values=[])
        self.combo_cat.pack(fill="x", padx=10, pady=(0, 8))

        # Proveedor (ComboBox)
        ctk.CTkLabel(self.frame_form, text="Proveedor:").pack(anchor="w", padx=10)
        self.combo_prov = ctk.CTkComboBox(self.frame_form, state="readonly", values=[])
        self.combo_prov.pack(fill="x", padx=10, pady=(0, 8))

        # Precio
        ctk.CTkLabel(self.frame_form, text="Precio ($):").pack(anchor="w", padx=10)
        self.entry_precio = ctk.CTkEntry(self.frame_form)
        self.entry_precio.pack(fill="x", padx=10, pady=(0, 8))

        # Stock actual
        ctk.CTkLabel(self.frame_form, text="Stock actual:").pack(anchor="w", padx=10)
        self.entry_stock = ctk.CTkEntry(self.frame_form)
        self.entry_stock.pack(fill="x", padx=10, pady=(0, 8))

        # Stock mínimo
        ctk.CTkLabel(self.frame_form, text="Stock mínimo de alerta:").pack(anchor="w", padx=10)
        self.entry_stock_min = ctk.CTkEntry(self.frame_form)
        self.entry_stock_min.pack(fill="x", padx=10, pady=(0, 12))

        # Botones de acción
        self.btn_guardar = ctk.CTkButton(
            self.frame_form, text="Guardar (Alta / Modificar)", command=self.guardar_producto
        )
        self.btn_guardar.pack(fill="x", padx=10, pady=4)

        self.btn_limpiar = ctk.CTkButton(
            self.frame_form, text="Nuevo / Limpiar formulario", fg_color="gray", command=self.limpiar_formulario
        )
        self.btn_limpiar.pack(fill="x", padx=10, pady=4)

        self.btn_eliminar = ctk.CTkButton(
            self.frame_form, text="Eliminar seleccionado", fg_color="#c0392b", hover_color="#922b21",
            command=self.eliminar_producto
        )
        self.btn_eliminar.pack(fill="x", padx=10, pady=4)

    def crear_tabla(self):
        self.frame_tabla = ctk.CTkFrame(self)
        self.frame_tabla.grid(row=0, column=1, pady=5, sticky="nsew")
        self.frame_tabla.grid_columnconfigure(0, weight=1)
        self.frame_tabla.grid_rowconfigure(1, weight=1)

        # Barra superior de búsqueda
        frame_busqueda = ctk.CTkFrame(self.frame_tabla, fg_color="transparent")
        frame_busqueda.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        frame_busqueda.grid_columnconfigure(0, weight=1)

        self.entry_buscar = ctk.CTkEntry(
            frame_busqueda, placeholder_text="Buscar por código o nombre..."
        )
        self.entry_buscar.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.buscar())

        btn_buscar = ctk.CTkButton(frame_busqueda, text="Buscar", width=90, command=self.buscar)
        btn_buscar.grid(row=0, column=1, padx=(0, 5))

        btn_ver_todos = ctk.CTkButton(
            frame_busqueda, text="Ver todos", width=90, fg_color="gray", command=self.ver_todos
        )
        btn_ver_todos.grid(row=0, column=2)

        # Tabla Treeview
        columnas = ("codigo", "nombre", "categoria", "proveedor", "precio", "stock", "minimo")
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")

        encabezados = {
            "codigo": ("Código", 70),
            "nombre": ("Nombre", 170),
            "categoria": ("Categoría", 110),
            "proveedor": ("Proveedor", 160),
            "precio": ("Precio ($)", 90),
            "stock": ("Stock", 65),
            "minimo": ("Mín.", 60),
        }
        for col, (texto, ancho) in encabezados.items():
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, anchor="center" if col in ("codigo", "precio", "stock", "minimo") else "w")

        # Color rojo para resaltar productos con stock menor al mínimo
        self.tabla.tag_configure("bajo", foreground="red")

        self.tabla.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="nsew")
        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar_fila)

        # Leyenda inferior
        ctk.CTkLabel(
            self.frame_tabla,
            text="Nota: Las filas en color ROJO indican productos con stock por debajo del mínimo.",
            text_color="#e74c3c", font=("Arial", 12, "italic")
        ).grid(row=2, column=0, padx=10, pady=(0, 8), sticky="w")

    def cargar_combos(self):
        """Carga las categorías y proveedores desde la BD en los desplegables."""
        categorias = db.listar_categorias()
        self.mapa_categorias = {nombre: id_cat for id_cat, nombre in categorias}
        nombres_cat = list(self.mapa_categorias.keys())
        self.combo_cat.configure(values=nombres_cat)
        if nombres_cat and not self.combo_cat.get():
            self.combo_cat.set(nombres_cat[0])

        proveedores = db.listar_proveedores()
        self.mapa_proveedores = {razon: id_prov for id_prov, cuit, razon, tel, email in proveedores}
        nombres_prov = list(self.mapa_proveedores.keys())
        self.combo_prov.configure(values=nombres_prov)
        if nombres_prov and not self.combo_prov.get():
            self.combo_prov.set(nombres_prov[0])

    def refrescar_tabla(self, lista_productos=None):
        """Limpia y vuelve a cargar los productos en el Treeview."""
        self.tabla.delete(*self.tabla.get_children())
        if lista_productos is None:
            lista_productos = db.listar_productos()

        self.productos_en_memoria = {}
        for prod in lista_productos:
            # prod: (id_producto, codigo, nombre, categoria, proveedor, precio, stock, stock_minimo, descripcion)
            id_prod = prod[0]
            self.productos_en_memoria[str(id_prod)] = prod
            stock = prod[6]
            stock_min = prod[7]
            tag = ("bajo",) if stock < stock_min else ()

            valores_fila = (prod[1], prod[2], prod[3], prod[4], f"{prod[5]:.2f}", stock, stock_min)
            self.tabla.insert("", "end", iid=str(id_prod), values=valores_fila, tags=tag)

    def al_seleccionar_fila(self, evento):
        """Carga los datos de la fila seleccionada en el formulario para poder editarla."""
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        iid = seleccion[0]
        prod = self.productos_en_memoria.get(iid)
        if not prod:
            return

        self.id_seleccionado = prod[0]

        self.entry_codigo.delete(0, "end")
        self.entry_codigo.insert(0, prod[1])

        self.entry_nombre.delete(0, "end")
        self.entry_nombre.insert(0, prod[2])

        self.combo_cat.set(prod[3])
        self.combo_prov.set(prod[4])

        self.entry_precio.delete(0, "end")
        self.entry_precio.insert(0, str(prod[5]))

        self.entry_stock.delete(0, "end")
        self.entry_stock.insert(0, str(prod[6]))

        self.entry_stock_min.delete(0, "end")
        self.entry_stock_min.insert(0, str(prod[7]))

        self.entry_descripcion.delete(0, "end")
        self.entry_descripcion.insert(0, prod[8] if prod[8] else "")

    def limpiar_formulario(self):
        """Vacía todas las cajas de texto y deselecciona la tabla para dar de alta un nuevo producto."""
        self.id_seleccionado = None
        self.tabla.selection_remove(self.tabla.selection())
        for entry in (
            self.entry_codigo, self.entry_nombre, self.entry_descripcion,
            self.entry_precio, self.entry_stock, self.entry_stock_min
        ):
            entry.delete(0, "end")

    def guardar_producto(self):
        """Valida los campos y guarda (inserta o actualiza) el producto en la base de datos."""
        codigo = self.entry_codigo.get().strip()
        nombre = self.entry_nombre.get().strip()
        descripcion = self.entry_descripcion.get().strip()
        nombre_cat = self.combo_cat.get()
        nombre_prov = self.combo_prov.get()

        if not codigo or not nombre or not nombre_cat or not nombre_prov:
            messagebox.showwarning("Datos incompletos", "Código, Nombre, Categoría y Proveedor son obligatorios.")
            return

        try:
            precio = float(self.entry_precio.get().replace(",", ".").strip())
            if precio <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Dato inválido", "El precio debe ser un número mayor a 0.")
            return

        try:
            stock = int(self.entry_stock.get().strip())
            stock_min = int(self.entry_stock_min.get().strip() or "0")
            if stock < 0 or stock_min < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Dato inválido", "El stock y el stock mínimo deben ser números enteros mayores o iguales a 0.")
            return

        id_categoria = self.mapa_categorias.get(nombre_cat)
        id_proveedor = self.mapa_proveedores.get(nombre_prov)

        try:
            if self.id_seleccionado is None:
                # Alta de nuevo producto
                db.insertar_producto(codigo, nombre, descripcion, precio, stock, stock_min, id_categoria, id_proveedor)
                messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            else:
                # Modificación de producto existente
                db.actualizar_producto(
                    codigo, nombre, descripcion, precio, stock, stock_min,
                    id_categoria, id_proveedor, self.id_seleccionado
                )
                messagebox.showinfo("Éxito", "Producto actualizado correctamente.")

            self.limpiar_formulario()
            self.refrescar_tabla()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error de duplicado", "Ya existe un producto con ese código o nombre.")
        except Exception as e:
            messagebox.showerror("Error de base de datos", f"Ocurrió un error inesperado:\n{e}")

    def eliminar_producto(self):
        """Elimina el producto seleccionado previa confirmación del usuario."""
        if self.id_seleccionado is None:
            messagebox.showwarning("Sin selección", "Seleccione primero un producto de la tabla para eliminar.")
            return

        codigo = self.entry_codigo.get()
        nombre = self.entry_nombre.get()
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar {codigo} – {nombre}?"
        )
        if confirmar:
            try:
                db.eliminar_producto(self.id_seleccionado)
                messagebox.showinfo("Eliminado", "Producto eliminado correctamente.")
                self.limpiar_formulario()
                self.refrescar_tabla()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el producto:\n{e}")

    def buscar(self):
        texto = self.entry_buscar.get().strip()
        if texto:
            resultados = db.buscar_productos(texto)
            self.refrescar_tabla(resultados)
        else:
            self.refrescar_tabla()

    def ver_todos(self):
        self.entry_buscar.delete(0, "end")
        self.refrescar_tabla()