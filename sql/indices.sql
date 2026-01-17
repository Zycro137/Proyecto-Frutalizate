-- Para reportes de ventas rápidos en intervalos o fechas específicas
CREATE INDEX idx_pedido_fecha ON pedido(fechaRealizado);

-- agilizar los reportes de las ventas de un producto específico
CREATE INDEX idx_detalle_pedido_producto ON detalle_pedido(producto_id);

-- Agilizar la búsqueda de todas las entregas de un repartidor para llevar un control
CREATE INDEX idx_pedido_repartidor ON pedido(repartidor_id);

-- Agiliza la clave foránea, cada pedido consulta sus detalles.
CREATE INDEX idx_detalle_pedido_pedido ON detalle_pedido(pedido_id);

-- Para reportes financieros en la tabla pagos buscando cada pedido
-- mediante la fk pedido_id
CREATE INDEX idx_pago_pedido ON pago(pedido_id);
