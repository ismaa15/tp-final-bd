-- prueba de stock < stock_minimo
SELECT codigo, nombre, stock, stock_minimo 
FROM productos 
WHERE stock < stock_minimo;

SELECT c.nombre AS categoria,
       COUNT(p.id_producto) AS cantidad_productos,
       SUM(p.precio * p.stock) AS valor_total_stock
FROM categorias c
LEFT JOIN productos p ON c.id_categoria = p.id_categoria
GROUP BY c.nombre;

SELECT pr.razon_social, pr.cuit
FROM proveedores pr
LEFT JOIN productos p ON pr.id_proveedor = p.id_proveedor
WHERE p.id_producto IS NULL;