DELIMITER /

CREATE TRIGGER descuento_stock_producto
AFTER INSERT ON Detalle_Pedido
FOR EACH ROW
BEGIN
    UPDATE Producto
    SET stock = stock - new.cantidad
    WHERE producto_id = new.producto_id;
END
/DELIMITER ;


DELIMITER /

CREATE TRIGGER validar_stock_negativo
BEFORE UPDATE ON Producto
FOR EACH ROW
BEGIN
    IF new.stock < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: El stock del producto no puede ser negativo';
    END IF;
END
/DELIMITER ;
