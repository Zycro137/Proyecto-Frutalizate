-- =======================================================
-- SENTENCIAS SQL PURAS EXTRAÍDAS DEL CÓDIGO DE PYTHON
-- =======================================================

-- -------------------------------------------------------
-- clientes.py
-- -------------------------------------------------------

-- 1. buscarClienteSuscripcion(cedula)
-- Busca datos del cliente y su ÚLTIMA suscripción (sea Activa o Cancelada)
SELECT 
    c.nombre, 
    c.apellido, 
    c.cliente_id, 
    c.telefono, 
    c.email,
    s.suscripcion_id, 
    s.frecuencia, 
    s.fecha_proxEntrega,
    s.estado
FROM Cliente c
LEFT JOIN Suscripcion s ON c.cliente_id = s.cliente_id
WHERE c.cliente_id = '0925465631'  -- Ejemplo de %s
ORDER BY s.suscripcion_id DESC
LIMIT 1;

-- 2. actualizarCliente(...)
UPDATE Cliente 
SET nombre = 'Ana', 
    apellido = 'Garcia', 
    telefono = '0991234567', 
    email = 'ana.new@email.com'
WHERE cliente_id = '0925465631';

-- 3. crearSuscripcion(...)
-- Inserta una nueva suscripción. El estado se fija manualmente como 'Activa'.
INSERT INTO Suscripcion (frecuencia, fecha_inicio, fecha_proxEntrega, estado, cliente_id) 
VALUES (7, CURDATE(), '2025-12-20', 'Activa', '0925465631');

-- 4. cancelarSuscripcion(suscripcion_id)
-- Realiza una baja lógica cambiando el estado, NO borra el registro.
UPDATE Suscripcion 
SET estado = 'Cancelada' 
WHERE suscripcion_id = 1;


-- -------------------------------------------------------
-- inventario.py
-- -------------------------------------------------------

-- 5. obtenerFrutas()
-- Une la tabla Frutas con Proveedor para mostrar el nombre del proveedor.
SELECT 
    f.frutas_id, 
    f.nombre, 
    f.stock, 
    p.nombre AS proveedor_nombre
FROM Frutas f
JOIN Proveedor p ON f.proveedor_id = p.proveedor_id;

-- 6. obtenerProductos()
-- Lista todos los productos terminados (Jugos).
SELECT producto_id, nombre, descripcion, precioUnitario, stock 
FROM Producto;

-- 7. buscarProductoPorId(id)
SELECT producto_id, nombre, descripcion, precioUnitario, stock 
FROM Producto 
WHERE producto_id = 1;

-- 8. buscarProductoPorNombre(nombre)
-- Usa LOWER() para hacer la búsqueda insensible a mayúsculas/minúsculas.
SELECT producto_id, nombre, descripcion, precioUnitario, stock 
FROM Producto 
WHERE LOWER(nombre) = LOWER('Jugo de Naranja');

-- 9. crearProducto(...)
-- Inserta un nuevo jugo. Nota: No incluye proveedor_id según tu código actual.
INSERT INTO Producto (nombre, descripcion, precioUnitario, stock)
VALUES ('Jugo Verde', 'Jugo detox de espinaca y manzana', 3.50, 10);

-- 10. actualizarProducto(...)
UPDATE Producto 
SET nombre = 'Jugo Verde Premium', 
    descripcion = 'Nueva receta con apio', 
    precioUnitario = 4.00, 
    stock = 15 
WHERE producto_id = 1;

-- 11. eliminarProducto(id)
-- Intenta borrar físicamente. Fallará si hay Pedidos vinculados (Integridad Referencial).
DELETE FROM Producto 
WHERE producto_id = 1;