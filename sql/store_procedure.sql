use bd_frutalizate;

#TABLA CLIENTES
#RESIGNAL ES PARA QUE EN PYTHON SE OBTENGA EL ERROR Y SE PUEDA MANEJAR
DELIMITER //

CREATE PROCEDURE insertCliente(IN p_id VARCHAR(255), IN p_nombre VARCHAR(255), IN p_apellido VARCHAR(255), IN p_telefono VARCHAR(255), IN p_email VARCHAR(255))
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL; 
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error al insertar cliente';
    END;

    START TRANSACTION;
    INSERT INTO Cliente(cliente_id, nombre, apellido, telefono, email)
    VALUES (p_id, p_nombre, p_apellido, p_telefono, p_email);
    COMMIT;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateCliente(IN p_id VARCHAR(255), IN p_telefono VARCHAR(255), IN p_email VARCHAR(255), IN p_nombre VARCHAR(255), IN p_apellido VARCHAR(255))
BEGIN
    DECLARE filas INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL; 
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error al actualizar cliente';
    END;

    START TRANSACTION;

    UPDATE Cliente SET nombre=p_nombre, apellido=p_apellido, telefono=p_telefono, email=p_email WHERE cliente_id=p_id;
    SET filas = ROW_COUNT();
    IF filas = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cliente no existe';
    END IF;

    COMMIT;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE deleteCliente(IN p_id VARCHAR(255))
BEGIN
    DECLARE filas INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL; 
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se puede eliminar el cliente';
    END;

    START TRANSACTION;

    DELETE FROM Cliente WHERE cliente_id = p_id;
    SET filas = ROW_COUNT();

    IF filas = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cliente no existe';
    END IF;

    COMMIT;
END//
DELIMITER ;

# TABLA PEDIDO

DELIMITER //
CREATE PROCEDURE insertPedido(IN p_fecha DATE, IN p_hora VARCHAR(255), IN p_direccion VARCHAR(255), IN p_cliente VARCHAR(255), IN p_repartidor INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL; 
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error al crear pedido';
    END;

    START TRANSACTION;
    INSERT INTO Pedido(fechaRealizado, horaEntrega, estado, direccion, cliente_id, repartidor_id)
    VALUES (p_fecha, p_hora, 'Pendiente', p_direccion, p_cliente, p_repartidor);
    COMMIT;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateEstadoPedido(IN p_id INT, IN p_estado VARCHAR(255))
BEGIN
    DECLARE filas INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL; 
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error al actualizar pedido';
    END;

    START TRANSACTION;
    UPDATE Pedido SET estado = p_estado WHERE pedido_id = p_id;

    SET filas = ROW_COUNT();
    IF filas = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Pedido no existe';
    END IF;

    COMMIT;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE deletePedido(IN p_id INT)
BEGIN
    DECLARE filas INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL; 
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede eliminar el pedido';
    END;

    START TRANSACTION;
    DELETE FROM Pedido WHERE pedido_id = p_id;
    
    SET filas = ROW_COUNT();
    IF filas = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Pedido no existe';
    END IF;

    COMMIT;
END//
DELIMITER ;

# TABLA SUSCRIPCION

DELIMITER //
CREATE PROCEDURE insertSuscripcion(IN p_cliente_id VARCHAR(255), IN p_frecuencia INT, IN p_fecha_prox DATE)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;   
    END;

    START TRANSACTION;

    INSERT INTO Suscripcion (frecuencia, fecha_inicio, fecha_proxEntrega, estado, cliente_id)
    VALUES (p_frecuencia, CURDATE(), p_fecha_prox, 'Activa', p_cliente_id);

    COMMIT;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateSuscripcion(IN p_sus_id INT, IN p_frecuencia INT, IN p_fecha_prox DATE)
BEGIN
    DECLARE filas_afectadas INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;
    UPDATE Suscripcion SET frecuencia = p_frecuencia, fecha_proxEntrega = p_fecha_prox WHERE suscripcion_id = p_sus_id;

    SET filas_afectadas = ROW_COUNT();
    IF filas_afectadas = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No existe la suscripción a actualizar';
    END IF;
    COMMIT;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE eliminarSuscripcion(IN p_sus_id INT)
BEGIN
    DECLARE filas_afectadas INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;
    DELETE FROM Suscripcion WHERE suscripcion_id = p_sus_id;

    SET filas_afectadas = ROW_COUNT();
    IF filas_afectadas = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No existe la suscripción a eliminar';
    END IF;
    COMMIT;
END//
DELIMITER ;

#TABLA PRODUCTO

DELIMITER //

CREATE PROCEDURE crearProducto(IN p_nombre VARCHAR(255), IN p_descripcion VARCHAR(255),IN p_precio FLOAT,IN p_stock INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;
    INSERT INTO Producto (nombre, descripcion, precioUnitario, stock)
    VALUES (p_nombre, p_descripcion, p_precio, p_stock);

    COMMIT;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateProducto(IN p_producto_id INT, IN p_nombre VARCHAR(255), IN p_descripcion VARCHAR(255), IN p_precio FLOAT, IN p_stock INT)
BEGIN
    DECLARE filas_afectadas INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;
    UPDATE Producto SET nombre = p_nombre, descripcion = p_descripcion, precioUnitario = p_precio, stock = p_stock WHERE producto_id = p_producto_id;

    SET filas_afectadas = ROW_COUNT();
    IF filas_afectadas = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No existe el producto a actualizar';
    END IF;

    COMMIT;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE deleteProducto(IN p_producto_id INT)
BEGIN
    DECLARE filas_afectadas INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;
    DELETE FROM Producto WHERE producto_id = p_producto_id;

    SET filas_afectadas = ROW_COUNT();
    IF filas_afectadas = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No existe el producto a eliminar';
    END IF;

    COMMIT;
END//
DELIMITER ;


