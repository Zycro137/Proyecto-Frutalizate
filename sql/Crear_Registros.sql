INSERT INTO Proveedor (nombre, telefono, direccion) VALUES 
('Frutas del Huerto S.A.', '0911223344', 'Km 12 Vía a la Costa'),
('AgroDistribuidora El Campo', '0999887766', 'Mercado Mayorista Bloque 5');

INSERT INTO Frutas (nombre, stock, proveedor_id) VALUES
('Manzana', 30, 1),
('Pera', 16, 1),
('Fresa', 20, 1),
('Uva', 60, 1),
('Mango', 25, 1),
('Banano', 24, 2),
('Naranja', 100, 2),
('Piña', 13, 2),
('Papaya', 10, 2),
('Sandía', 5, 2);

INSERT INTO Producto (nombre, descripcion, precioUnitario, stock) VALUES
('Jugo de Manzana',
 'Jugo natural elaborado únicamente con manzana',
 2.50, 8),

('Jugo de Naranja',
 'Jugo natural elaborado únicamente con naranja',
 2.40, 7),

('Jugo de Banano',
 'Jugo natural elaborado únicamente con banano',
 2.60, 6),

('Jugo de Fresa',
 'Jugo natural elaborado únicamente con fresa',
 2.80, 5),

('Jugo de Mango',
 'Jugo natural elaborado únicamente con mango',
 2.70, 6),

('Jugo de Piña',
 'Jugo natural elaborado únicamente con piña',
 2.60, 5),

('Jugo de Manzana y Pera',
 'Jugo natural elaborado con manzana y pera',
 3.00, 4),

('Jugo Tropical',
 'Jugo natural elaborado con mango, piña y naranja',
 3.20, 3),

('Jugo Energético',
 'Jugo natural elaborado con banano, fresa y papaya',
 3.30, 3),

('Jugo Refrescante',
 'Jugo natural elaborado con sandía y naranja',
 3.10, 4);

INSERT INTO Producto_Fruta (producto_id, frutas_id) VALUES
-- Jugos simples
(1, 1),   -- Jugo de Manzana → Manzana
(2, 7),   -- Jugo de Naranja → Naranja
(3, 6),   -- Jugo de Banano → Banano
(4, 3),   -- Jugo de Fresa → Fresa
(5, 5),   -- Jugo de Mango → Mango
(6, 8),   -- Jugo de Piña → Piña

-- Jugos combinados
(7, 1),   -- Jugo Manzana y Pera → Manzana
(7, 2),   -- Jugo Manzana y Pera → Pera

(8, 5),   -- Jugo Tropical → Mango
(8, 8),   -- Jugo Tropical → Piña
(8, 7),   -- Jugo Tropical → Naranja

(9, 6),   -- Jugo Energético → Banano
(9, 3),   -- Jugo Energético → Fresa
(9, 9),   -- Jugo Energético → Papaya

(10,10),  -- Jugo Refrescante → Sandía
(10,7);   -- Jugo Refrescante → Naranja

INSERT INTO Cliente (cliente_id, nombre, apellido, telefono, email) VALUES
('0925465631', 'Ana', 'García', '0991234567', 'ana.g@email.com'),
('0957658798', 'Carlos', 'Mendoza', '0987654321', 'carlos.m@email.com'),
('0998723121', 'Lucía', 'Torres', '0957516985', 'lucia.torres@email.com'),
('0931775076', 'Bianka', 'Cañarte', '0924865132', 'bianka.c@email.com'),
('0943922286', 'Valeria', 'Monroy', '0944854962', 'valeria.m@email.com'),
('0951187129', 'Diego', 'Vélez', '099896531', 'diego.v@email.com'),
('0930257779', 'Sebastian', 'Salazar', '0996317826', 'sebastian.s@email.com'),
('0930329586', 'Matias', 'Mega', '0984172273', 'matias.m@email.com'),
('1316610524', 'Ariana', 'Esmeraldas', '0989379296', 'ariana.e@email.com'),
('0954794822', 'Sheryl', 'Tejena', '0995259402', 'sheryl.t@email.com');


select * from pedido;

INSERT INTO Suscripcion (frecuencia, fecha_inicio, fecha_proxEntrega, estado, cliente_id) VALUES
(7, '2025-12-01', '2025-12-08', 'Activa', '0925465631'),  
(NULL, NULL, NULL, NULL,'0957658798'),                                     
(NULL, NULL, NULL, NULL,'0998723121'),                                     
(14, '2025-11-25', '2025-12-09', 'Activa','0931775076'),  
(NULL, NULL, NULL, NULL,'0943922286'),                                     
(30, '2025-12-01', '2025-12-31', 'Activa','0951187129'),       
(NULL, NULL, NULL, NULL,'0930257779'),                                     
(NULL, NULL, NULL, NULL,'0930329586'),                                     
(7, '2025-12-03', '2025-12-10', 'Activa','1316610524'),                
(NULL, NULL, NULL, NULL,'0954794822');     


INSERT INTO Suscripcion_Detalle (cantidad, subtotal, producto_id, suscripcion_id) VALUES
(2, 5.00, 1, 1),   
(1, 3.20, 8, 1),   
(1, 3.00, 7, 4),   
(3, 7.80, 6, 6),   
(1, 2.50, 1, 9);   

INSERT INTO Repartidor (nombre, apellido, telefono) VALUES
('Jorge', 'Véliz', '0991122334'),
('Miguel', 'Andrade', '0982233445'),
('Carlos', 'Paredes', '0973344556'),
('Luis', 'Morales', '0964455667'),
('Fernando', 'Cedeño', '0955566778');

INSERT INTO Pedido (fechaRealizado, horaEntrega, estado, direccion, cliente_id, repartidor_id, suscripcion_id) VALUES
('2025-12-05', '14:30:00', 'Entregado', 'Cdla. Kennedy Norte', '0925465631', 1, 1),
('2025-12-06', '12:15:00', 'Entregado', 'Urdesa Central',      '0957658798', 2, NULL),
('2025-12-07', '09:45:00', 'Entregado', 'Alborada 10ma Etapa', '0998723121', 3, NULL),
('2025-12-05', '18:20:00', 'Entregado', 'Samborondón Centro',  '0931775076', 4, 4),
('2025-12-08', '13:10:00', 'Entregado', 'Centro Norte',        '0951187129', 5, 6),
('2025-12-09', '20:00:00', 'Entregado', 'Guasmo Sur',          '0930257779', 1, NULL),
('2025-12-09', '15:30:00', 'Entregado', 'Sauces 6',            '0930329586', 2, NULL),
('2025-12-10', '11:05:00', 'Entregado', 'Durán',               '1316610524', 3, 9),
('2025-12-10', '19:45:00', 'Entregado', 'La Florida',          '0954794822', 4, NULL),
('2025-12-11', '10:20:00', 'Entregado', 'Cdla. Kennedy Norte', '0925465631', 5, 1);

INSERT INTO Detalle_Pedido (cantidad, subtotal, pedido_id, producto_id) VALUES
-- Pedido 1
(2, 5.00, 1, 1),  
(1, 3.20, 1, 8),  

-- Pedido 2
(1, 2.40, 2, 2),  
(1, 2.60, 2, 3),  

-- Pedido 3
(1, 2.80, 3, 4),  

-- Pedido 4
(1, 3.00, 4, 7),  
(1, 2.70, 4, 5),  

-- Pedido 5
(2, 5.20, 5, 6),  
(1, 3.20, 5, 8),  

-- Pedido 6
(1, 2.60, 6, 3),  

-- Pedido 7
(1, 2.50, 7, 1),  
(1, 2.40, 7, 2),  

-- Pedido 8
(1, 2.50, 8, 1), 

-- Pedido 9
(1, 3.10, 9, 10), 
(1, 2.40, 9, 2),  

-- Pedido 10
(1, 3.00, 10, 7), 
(2, 5.20, 10, 6); 

INSERT INTO Pago (metodo, montototal, pedido_id) VALUES
('Efectivo', 8.20, 1),

('Transferencia', 5.00,  2),

('Tarjeta', 2.80,  3),

('Efectivo', 5.70,  4),

('Transferencia', 8.40,  5),

('Aplicación', 2.60,  6),

('Tarjeta', 4.90,  7),

('Transferencia', 2.50, 8),

('Efectivo', 5.50,  9),

('Tarjeta', 8.20,  10);
