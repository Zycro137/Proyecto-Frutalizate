-- Métodos de Python funcionales en MySql:


-- registrarCliente(cedula, nombre, apellido, telefono, email)
-- En Python usamos %s, aquí pongo valores de ejemplo
INSERT INTO Cliente (cliente_id, nombre, apellido, telefono, email)
VALUES ('0925465631', 'Juan', 'Perez', '0991234567', 'juan.perez@email.com');


-- crearSuscripcion(cedula, frecuencia, fecha, direccion)
-- Nota: El estado se inserta por defecto como 'Activa' si no se especifica
INSERT INTO Suscripcion (cliente_id, frecuencia, fecha_proxEntrega, estado, direccion)
VALUES ('0925465631', 'Semanal', '2023-11-01', 'Activa', 'Av. Principal 123 y Calle 2');


-- buscarClienteSuscripcion(cedula)
-- Esta es la consulta principal para verificar el estado del usuario
SELECT 
        c.nombre, 
        c.apellido, 
        c.cliente_id, 
        c.telefono, 
        c.email,
        s.suscripcion_id, 
        s.frecuencia, 
        s.fecha_proxEntrega,
        s.estado,
        s.direccion 
    FROM Cliente c
    LEFT JOIN Suscripcion s ON c.cliente_id = s.cliente_id
    WHERE c.cliente_id = '0925465631'; -- O la cédula que sea


-- actualizarFechaEntrega(suscripcion_id, nueva_fecha)
-- Usado cuando el cliente pide reagendar
UPDATE Suscripcion
SET fecha_proxEntrega = '2023-11-08'
WHERE suscripcion_id = 1;


-- cambiarEstadoSuscripcion(suscripcion_id, nuevo_estado)
-- Usado para 'Pausar' o 'Cancelar' sin borrar el registro histórico
UPDATE Suscripcion
SET estado = 'Cancelada'
WHERE suscripcion_id = 1;


-- actualizarDireccion(cliente_id, nueva_direccion)
-- Actualiza la dirección de la suscripción activa más reciente del cliente
UPDATE Suscripcion
SET direccion = 'Calle Nueva 456'
WHERE cliente_id = '0925465631' AND estado = 'Activa';
    
    
    
    