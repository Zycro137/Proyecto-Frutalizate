CREATE VIEW reporte_PedidosCliente AS
SELECT 
    p.pedido_id,
    c.nombre AS nombre_cliente,
    c.apellido AS apellido_cliente,
    p.fechaRealizado,
    p.estado,
    pg.metodo,
    pg.montototal
FROM Pedido p
JOIN Cliente c ON p.cliente_id = c.cliente_id
JOIN Pago pg ON p.pedido_id = pg.pedido_id;


CREATE VIEW reporte_DetallePedido AS
SELECT 
    p.pedido_id,
    prod.nombre AS producto,
    dp.cantidad,
    dp.subtotal,
    p.estado
FROM Detalle_Pedido dp
JOIN Producto prod ON dp.producto_id = prod.producto_id
JOIN Pedido p ON dp.pedido_id = p.pedido_id;


CREATE VIEW reporte_suscripciones AS
SELECT 
    s.suscripcion_id,
    c.nombre,
    c.apellido,
    prod.nombre AS producto,
    sd.cantidad,
    s.frecuencia,
    s.estado
FROM Suscripcion s
JOIN Cliente c ON s.cliente_id = c.cliente_id
JOIN Suscripcion_Detalle sd ON s.suscripcion_id = sd.suscripcion_id
JOIN Producto prod ON sd.producto_id = prod.producto_id
WHERE s.estado = 'Activa';


CREATE VIEW reporte_frutas AS
SELECT 
    prod.nombre AS producto,
    f.nombre AS fruta,
    pr.nombre AS proveedor,
    f.stock AS stock_fruta
FROM Producto prod
JOIN Producto_Fruta pf ON prod.producto_id = pf.producto_id
JOIN Frutas f ON pf.frutas_id = f.frutas_id
JOIN Proveedor pr ON f.proveedor_id = pr.proveedor_id;

