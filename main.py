import customtkinter as ctk
import db
from ui.ventana_producto import FrameProductos
from ui.ventana_categoria import FrameCategorias

# Configuración visual de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Inventario - Distribuidora del Litoral")
        self.geometry("1150x680")

        # Contenedor de pestañas (Tabview)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Pestañas
        tab_prod = self.tabview.add("Productos")
        tab_cat = self.tabview.add("Categorías y Proveedores")

        # Vista de Productos en la pestaña 1
        self.vista_productos = FrameProductos(tab_prod)
        self.vista_productos.pack(fill="both", expand=True)

        # Vista de Categorías y Proveedores en la pestaña 2
        # Le pasamos self.vista_productos.cargar_combos para que al crear una categoría/proveedor
        # se actualicen automáticamente las listas desplegables en la pestaña de Productos
        self.vista_categorias = FrameCategorias(
            tab_cat,
            al_cambiar_datos=self.vista_productos.cargar_combos
        )
        self.vista_categorias.pack(fill="both", expand=True)


if __name__ == "__main__":
    db.inicializar_base()
    app = VentanaPrincipal()
    app.mainloop()