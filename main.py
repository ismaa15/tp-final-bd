import customtkinter as ctk
from tkinter import ttk, messagebox
# import db (Aquí importarás tu módulo de base de datos)

# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Inventario - Distribuidora del Litoral")
        self.geometry("1050x600")
        
        # Grid layout: 1 fila, 2 columnas
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_formulario()
        self.crear_tabla()

    def crear_formulario(self):
        # Frame izquierdo para el formulario
        self.frame_form = ctk.CTkFrame(self, width=300)
        self.frame_form.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        
        ctk.CTkLabel(self.frame_form, text="Datos del producto", font=("Arial", 16, "bold")).pack(pady=10)

        # Campos (Ejemplo con Código y Nombre)
        ctk.CTkLabel(self.frame_form, text="Código:").pack(anchor="w", padx=10)
        self.entry_codigo = ctk.CTkEntry(self.frame_form)
        self.entry_codigo.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(self.frame_form, text="Nombre:").pack(anchor="w", padx=10)
        self.entry_nombre = ctk.CTkEntry(self.frame_form)
        self.entry_nombre.pack(fill="x", padx=10, pady=(0, 10))

        # Combobox para Categoría (Debe cargarse desde la DB)
        ctk.CTkLabel(self.frame_form, text="Categoría:").pack(anchor="w", padx=10)
        self.combo_cat = ctk.CTkComboBox(self.frame_form, values=["Almacén", "Bebidas", "Limpieza"]) 
        self.combo_cat.pack(fill="x", padx=10, pady=(0, 10))

        # Botones de acción[cite: 5]
        self.btn_guardar = ctk.CTkButton(self.frame_form, text="Guardar", command=self.guardar_producto)
        self.btn_guardar.pack(pady=10)
        
        self.btn_eliminar = ctk.CTkButton(self.frame_form, text="Eliminar", fg_color="red", hover_color="darkred")
        self.btn_eliminar.pack(pady=5)

    def crear_tabla(self):
        # Frame derecho para la tabla y búsqueda
        self.frame_tabla = ctk.CTkFrame(self)
        self.frame_tabla.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_tabla.grid_columnconfigure(0, weight=1)
        self.frame_tabla.grid_rowconfigure(1, weight=1)

        # Barra de búsqueda[cite: 5]
        self.entry_buscar = ctk.CTkEntry(self.frame_tabla, placeholder_text="Buscar código o nombre...")
        self.entry_buscar.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Configuración del Treeview estándar dentro de CTk[cite: 5]
        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")
        
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
        
        # Etiqueta para resaltar filas con stock bajo
        self.tabla.tag_configure("bajo", foreground="red")
        
        self.tabla.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def guardar_producto(self):
        # Ejemplo de validación básica[cite: 5]
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Dato faltante", "El código es obligatorio.") #[cite: 9]
            return
        # Aquí iría el bloque try/except para capturar errores de formato o base de datos[cite: 9]

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()