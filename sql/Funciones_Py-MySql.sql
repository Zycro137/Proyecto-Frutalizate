-- Métodos de Python funcionales en MySql:

-- buscarClienteSuscripcion(cedula)
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
    
    
    select * from suscripcion;
    select * from cliente;
    SELECT * FROM producto
    
    
    