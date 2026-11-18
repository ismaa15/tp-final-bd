import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3
import db


class FrameCategorias(ctk.CTkFrame):
    def __init__(self, master, al_cambiar_datos=None):
        super().__init__(master, fg_color="transparent")
        # Función callback para avisarle a la pestaña de productos que actualice sus ComboBox
        self.al_cambiar_datos = al_cambiar_datos

        # Dividimos en 2 columnas iguales: izquierda Categorías, derecha Proveedores
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.crear_panel_categorias()
        self.crear_panel_proveedores()

        self.refrescar_categorias()
        self.refrescar_proveedores()

    # ==========================================
    # PANEL IZQUIERDO: CATEGORÍAS
    # ==========================================
    def crear_panel_categorias(self):
        frame_cat = ctk.CTkFrame(self)
        frame_cat.grid(row=0, column=0, padx=(0, 8), pady=5, sticky="nsew")
        frame_cat.grid_columnconfigure(0, weight=1)
        frame_cat.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(frame_cat, text="Gestión de Categorías", font=("Arial", 16, "bold")).grid(
            row=0, column=0, pady=10
        )

        # Formulario de categoría
        form_cat = ctk.CTkFrame(frame_cat, fg_color="transparent")
        form_cat.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        form_cat.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(form_cat, text="Nombre:").grid(row=0, column=0, padx=(0, 8), pady=5)
        self.entry_nom_cat = ctk.CTkEntry(form_cat, placeholder_text="Ej: Lácteos")
        self.entry_nom_cat.grid(row=0, column=1, pady=5, sticky="ew")

        btn_frame = ctk.CTkFrame(form_cat, fg_color="transparent")
        btn_frame.grid(row=1, column=0, columnspan=2, pady=8)

        ctk.CTkButton(btn_frame, text="Agregar Categoría", width=140, command=self.guardar_categoria).pack(
            side="left", padx=5
        )
        ctk.CTkButton(
            btn_frame, text="Eliminar", width=100, fg_color="#c0392b", hover_color="#922b21",
            command=self.borrar_categoria
        ).pack(side="left", padx=5)

        # Tabla de categorías
        self.tabla_cat = ttk.Treeview(frame_cat, columns=("id", "nombre"), show="headings")
        self.tabla_cat.heading("id", text="ID")
        self.tabla_cat.column("id", width=50, anchor="center")
        self.tabla_cat.heading("nombre", text="Nombre de Categoría")
        self.tabla_cat.column("nombre", width=180)
        self.tabla_cat.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    def refrescar_categorias(self):
        self.tabla_cat.delete(*self.tabla_cat.get_children())
        for id_cat, nombre in db.listar_categorias():
            self.tabla_cat.insert("", "end", iid=str(id_cat), values=(id_cat, nombre))

    def guardar_categoria(self):
        nombre = self.entry_nom_cat.get().strip()
        if not nombre:
            messagebox.showwarning("Dato faltante", "Ingrese el nombre de la categoría.")
            return
        try:
            db.insertar_categoria(nombre)
            self.entry_nom_cat.delete(0, "end")
            self.refrescar_categorias()
            if self.al_cambiar_datos:
                self.al_cambiar_datos()
            messagebox.showinfo("Éxito", "Categoría agregada correctamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ya existe una categoría con ese nombre.")

    def borrar_categoria(self):
        seleccion = self.tabla_cat.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Seleccione una categoría de la tabla para eliminar.")
            return
        id_cat = int(seleccion[0])
        nombre = self.tabla_cat.item(seleccion[0], "values")[1]

        if messagebox.askyesno("Confirmar", f"¿Eliminar la categoría '{nombre}'?"):
            try:
                db.eliminar_categoria(id_cat)
                self.refrescar_categorias()
                if self.al_cambiar_datos:
                    self.al_cambiar_datos()
                messagebox.showinfo("Eliminada", "Categoría eliminada correctamente.")
            except sqlite3.IntegrityError:
                messagebox.showerror(
                    "Acción bloqueada",
                    f"No se puede eliminar la categoría '{nombre}' porque tiene productos asociados."
                )

    # ==========================================
    # PANEL DERECHO: PROVEEDORES
    # ==========================================
    def crear_panel_proveedores(self):
        frame_prov = ctk.CTkFrame(self)
        frame_prov.grid(row=0, column=1, padx=(8, 0), pady=5, sticky="nsew")
        frame_prov.grid_columnconfigure(0, weight=1)
        frame_prov.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(frame_prov, text="Gestión de Proveedores", font=("Arial", 16, "bold")).grid(
            row=0, column=0, pady=10
        )

        # Formulario de proveedor
        form_prov = ctk.CTkFrame(frame_prov, fg_color="transparent")
        form_prov.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        form_prov.grid_columnconfigure(1, weight=1)
        form_prov.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(form_prov, text="Razón Social:").grid(row=0, column=0, padx=5, pady=4, sticky="w")
        self.entry_razon = ctk.CTkEntry(form_prov)
        self.entry_razon.grid(row=0, column=1, padx=5, pady=4, sticky="ew")

        ctk.CTkLabel(form_prov, text="CUIT:").grid(row=0, column=2, padx=5, pady=4, sticky="w")
        self.entry_cuit = ctk.CTkEntry(form_prov, placeholder_text="30-12345678-9")
        self.entry_cuit.grid(row=0, column=3, padx=5, pady=4, sticky="ew")

        ctk.CTkLabel(form_prov, text="Teléfono:").grid(row=1, column=0, padx=5, pady=4, sticky="w")
        self.entry_tel = ctk.CTkEntry(form_prov)
        self.entry_tel.grid(row=1, column=1, padx=5, pady=4, sticky="ew")

        ctk.CTkLabel(form_prov, text="Email:").grid(row=1, column=2, padx=5, pady=4, sticky="w")
        self.entry_email = ctk.CTkEntry(form_prov)
        self.entry_email.grid(row=1, column=3, padx=5, pady=4, sticky="ew")

        btn_frame = ctk.CTkFrame(form_prov, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=4, pady=8)

        ctk.CTkButton(btn_frame, text="Agregar Proveedor", width=150, command=self.guardar_proveedor).pack(
            side="left", padx=5
        )
        ctk.CTkButton(
            btn_frame, text="Eliminar Proveedor", width=140, fg_color="#c0392b", hover_color="#922b21",
            command=self.borrar_proveedor
        ).pack(side="left", padx=5)

        # Tabla de proveedores
        cols = ("id", "cuit", "razon_social", "telefono", "email")
        self.tabla_prov = ttk.Treeview(frame_prov, columns=cols, show="headings")
        self.tabla_prov.heading("id", text="ID")
        self.tabla_prov.column("id", width=40, anchor="center")
        self.tabla_prov.heading("cuit", text="CUIT")
        self.tabla_prov.column("cuit", width=110, anchor="center")
        self.tabla_prov.heading("razon_social", text="Razón Social")
        self.tabla_prov.column("razon_social", width=160)
        self.tabla_prov.heading("telefono", text="Teléfono")
        self.tabla_prov.column("telefono", width=110)
        self.tabla_prov.heading("email", text="Email")
        self.tabla_prov.column("email", width=170)

        self.tabla_prov.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    def refrescar_proveedores(self):
        self.tabla_prov.delete(*self.tabla_prov.get_children())
        for prov in db.listar_proveedores():
            self.tabla_prov.insert("", "end", iid=str(prov[0]), values=prov)

    def guardar_proveedor(self):
        razon = self.entry_razon.get().strip()
        cuit = self.entry_cuit.get().strip()
        tel = self.entry_tel.get().strip()
        email = self.entry_email.get().strip()

        if not razon or not cuit:
            messagebox.showwarning("Datos faltantes", "La Razón Social y el CUIT son obligatorios.")
            return
        try:
            db.insertar_proveedor(cuit, razon, tel, email)
            for entry in (self.entry_razon, self.entry_cuit, self.entry_tel, self.entry_email):
                entry.delete(0, "end")
            self.refrescar_proveedores()
            if self.al_cambiar_datos:
                self.al_cambiar_datos()
            messagebox.showinfo("Éxito", "Proveedor agregado correctamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ya existe un proveedor con ese CUIT o Razón Social.")

    def borrar_proveedor(self):
        seleccion = self.tabla_prov.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Seleccione un proveedor de la tabla para eliminar.")
            return
        id_prov = int(seleccion[0])
        razon = self.tabla_prov.item(seleccion[0], "values")[2]

        if messagebox.askyesno("Confirmar", f"¿Eliminar el proveedor '{razon}'?"):
            try:
                db.eliminar_proveedor(id_prov)
                self.refrescar_proveedores()
                if self.al_cambiar_datos:
                    self.al_cambiar_datos()
                messagebox.showinfo("Eliminado", "Proveedor eliminado correctamente.")
            except sqlite3.IntegrityError:
                messagebox.showerror(
                    "Acción bloqueada",
                    f"No se puede eliminar el proveedor '{razon}' porque tiene productos asociados."
                )