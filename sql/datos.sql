PRAGMA foreign_keys = ON;

insert into categorias (nombre) values ('Almacen');
insert into categorias (nombre) values ('Bebidas');
insert into categorias (nombre) values ('Perfumeria');
insert into categorias (nombre) values ('Limpieza');

insert into proveedores (cuit, razon_social, telefono, email) values ('30-71234567-8', 'Molinos del Este S.A.', '0345-421-1000', 'ventas@molinosdeleste.com.ar');
insert into proveedores (cuit, razon_social, telefono, email) values ('30-70987654-3', 'Bebidas Mesopotamia SRL', '0345-422-2000', 'pedidos@bebidasmeso.com.ar');
insert into proveedores (cuit, razon_social, telefono, email) values ('30-69876543-1', 'Quimica Uruguay S.A.', '0345-423-3000', 'contacto@quimicauruguay.com.ar');

insert into productos (nombre, codigo, descripcion, precio, stock, stock_minimo, id_categoria, id_proveedor) values ('Yerba mate 1kg', 'P001', 'Yerba mate', 4500.00, 48, 10, 1, 1);
insert into productos (nombre, codigo, descripcion, precio, stock, stock_minimo, id_categoria, id_proveedor) values ('Aceite de girasol 1.5L', 'P002', 'Aceite de girasol', 3200.00, 30, 8, 1, 1);
insert into productos (nombre, codigo, descripcion, precio, stock, stock_minimo, id_categoria, id_proveedor) values ('Fideos tirabuzon 500g', 'P003', 'Fideos tirabuzon', 1450.00, 70, 15, 1, 1);
insert into productos (nombre, codigo, descripcion, precio, stock, stock_minimo, id_categoria, id_proveedor) values ('Gaseosa cola 2.25L', 'P004', 'Gaseosa cola', 2900.00, 60, 12, 2, 2);
insert into productos (nombre, codigo, descripcion, precio, stock, stock_minimo, id_categoria, id_proveedor) values ('Agua mineral 2L', 'P005', 'Agua mineral', 1300.00, 2, 10, 2, 2);
insert into productos (nombre, codigo, descripcion, precio, stock, stock_minimo, id_categoria, id_proveedor) values ('Lavandina 2L', 'P006', 'Lavandina', 1800.00, 4, 6, 4, 3);
insert into productos (nombre, codigo, descripcion, precio, stock, stock_minimo, id_categoria, id_proveedor) values ('Detergente 750ml', 'P007', 'Detergente', 2100.00, 25, 6, 4, 3);
insert into productos (nombre, codigo, descripcion, precio, stock, stock_minimo, id_categoria, id_proveedor) values ('Jabon de tocador x3', 'P008', 'Jabon de tocador', 2600.00, 18, 5, 4, 3);