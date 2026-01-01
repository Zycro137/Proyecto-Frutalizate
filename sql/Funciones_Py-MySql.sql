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

-- [NUEVO] CRUD ADMIN CLIENTES

-- 5. obtenerClientes()
-- Lista básica para la tabla de administración.
SELECT cliente_id, nombre, apellido, telefono, email FROM Cliente;

-- 6. crearCliente(...)
INSERT INTO Cliente (cliente_id, nombre, apellido, telefono, email)
VALUES ('0999999999', 'Nuevo', 'Cliente', '0912345678', 'nuevo@email.com');

-- 7. eliminarCliente(cedula)
-- Intenta borrar físicamente. Fallará si tiene integridad referencial (pedidos/suscripciones).
DELETE FROM Cliente WHERE cliente_id = '0925465631';

-- [NUEVO] CRUD ADMIN SUSCRIPCIONES

-- 8. obtenerTodasSuscripciones()
-- Join para ver de quién es cada suscripción en el panel admin.
SELECT 
    s.suscripcion_id,
    c.nombre,
    c.apellido,
    s.frecuencia,
    s.fecha_proxEntrega,
    s.estado,
    s.cliente_id
FROM Suscripcion s
JOIN Cliente c ON s.cliente_id = c.cliente_id
ORDER BY s.suscripcion_id DESC;

-- 9. obtenerSuscripcionPorId(id)
-- Usado para recuperar datos antes de editar (mostrar valor actual).
SELECT frecuencia, fecha_proxEntrega FROM Suscripcion WHERE suscripcion_id = 1;

-- 10. actualizarSuscripcion(...)
-- Permite editar frecuencia y fecha.
UPDATE Suscripcion 
SET frecuencia = 15, fecha_proxEntrega = '2026-01-15'
WHERE suscripcion_id = 1;

-- 11. eliminarSuscripcionFisica(id)
-- Borrado real. Fallará si tiene pedidos asociados.
DELETE FROM Suscripcion WHERE suscripcion_id = 1;


-- -------------------------------------------------------
-- inventario.py
-- -------------------------------------------------------

-- 12. obtenerFrutas()
-- Une la tabla Frutas con Proveedor para mostrar el nombre del proveedor.
SELECT 
    f.frutas_id, 
    f.nombre, 
    f.stock, 
    p.nombre AS proveedor_nombre
FROM Frutas f
JOIN Proveedor p ON f.proveedor_id = p.proveedor_id;

-- 13. obtenerProductos()
-- Lista todos los productos terminados (Jugos).
SELECT producto_id, nombre, descripcion, precioUnitario, stock 
FROM Producto;

-- 14. buscarProductoPorId(id)
SELECT producto_id, nombre, descripcion, precioUnitario, stock 
FROM Producto 
WHERE producto_id = 1;

-- 15. buscarProductoPorNombre(nombre)
-- Usa LOWER() para hacer la búsqueda insensible a mayúsculas/minúsculas.
SELECT producto_id, nombre, descripcion, precioUnitario, stock 
FROM Producto 
WHERE LOWER(nombre) = LOWER('Jugo de Naranja');

-- 16. crearProducto(...)
-- Inserta un nuevo jugo.
INSERT INTO Producto (nombre, descripcion, precioUnitario, stock)
VALUES ('Jugo Verde', 'Jugo detox de espinaca y manzana', 3.50, 10);

-- 17. actualizarProducto(...)
UPDATE Producto 
SET nombre = 'Jugo Verde Premium', 
    descripcion = 'Nueva receta con apio', 
    precioUnitario = 4.00, 
    stock = 15 
WHERE producto_id = 1;

-- 18. eliminarProducto(id)
-- Intenta borrar físicamente. Fallará si hay Pedidos vinculados.
DELETE FROM Producto 
WHERE producto_id = 1;


-- -------------------------------------------------------
-- pedidos.py (NUEVO MÓDULO)
-- -------------------------------------------------------

-- 19. obtenerPedidos()
-- Join triple: Pedido -> Cliente (obligatorio) -> Repartidor (opcional)
SELECT 
    p.pedido_id,
    p.fechaRealizado,
    p.horaEntrega,
    p.estado,
    c.nombre,
    c.apellido,
    r.nombre
FROM Pedido p
JOIN Cliente c ON p.cliente_id = c.cliente_id
LEFT JOIN Repartidor r ON p.repartidor_id = r.repartidor_id
ORDER BY p.pedido_id DESC;

-- 20. obtenerRepartidores()
SELECT repartidor_id, nombre, apellido FROM Repartidor;

-- 21. obtenerDetallePedido(id)
-- Ver qué productos tiene un pedido específico.
SELECT 
    dp.cantidad,
    dp.subtotal,
    prod.nombre
FROM Detalle_Pedido dp
JOIN Producto prod ON dp.producto_id = prod.producto_id
WHERE dp.pedido_id = 1;

-- 22. crearPedidoCompleto(...) 
-- ESTO ES UNA TRANSACCIÓN: Se ejecutan 3 pasos secuenciales.

    -- Paso A: Insertar Encabezado
    INSERT INTO Pedido (fechaRealizado, horaEntrega, estado, direccion, cliente_id, repartidor_id)
    VALUES (CURDATE(), '14:30:00', 'Pendiente', 'Av. Siempre Viva', '0925465631', 1);

    -- Paso B: Insertar Detalle (Se repite por cada producto en el carrito)
    INSERT INTO Detalle_Pedido (cantidad, subtotal, pedido_id, producto_id, estado)
    VALUES (2, 5.00, 1, 10, 'Pendiente'); 

    -- Paso C: Descontar Stock (Se repite por cada producto)
    UPDATE Producto SET stock = stock - 2 WHERE producto_id = 10;

-- 23. actualizarEstadoPedido(...)
UPDATE Pedido SET estado = 'Entregado' WHERE pedido_id = 1;

-- 24. eliminarPedido(id)
-- BORRADO EN CASCADA MANUAL (Orden estricto para evitar error FK).
    -- Paso A: Borrar detalles (hijos)
    DELETE FROM Detalle_Pedido WHERE pedido_id = 1;
    -- Paso B: Borrar pagos (hijos) - CRITICO para evitar error de constraint
    DELETE FROM Pago WHERE pedido_id = 1;
    -- Paso C: Borrar encabezado (padre)
    DELETE FROM Pedido WHERE pedido_id = 1;