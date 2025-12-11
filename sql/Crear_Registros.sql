-- Registros de Clientes
INSERT INTO Cliente (nombre, apellido, telefono, email) VALUES 
('Ana', 'García', '0991234567', 'ana.garcia@email.com'),
('Carlos', 'Mendoza', '0987654321', 'carlos.m@email.com'),
('Lucía', 'Torres', '0955555555', 'lucia.torres@email.com');



-- Registros de Proveedores
INSERT INTO Proveedor (nombre, telefono, direccion) VALUES 
('Frutas del Huerto S.A.', '0911223344', 'Km 12 Vía a la Costa'),
('AgroDistribuidora El Campo', '0999887766', 'Mercado Mayorista Bloque 5');



-- Registros de Repartidores
INSERT INTO Repartidor (nombre, apellido, telefono) VALUES 
('Jorge', 'Véliz', '0991112233'),
('Miguel', 'Andrade', '0988887766'),
('Sofía', 'López', '0977771234');



-- Registros de Productos (Jugos)
INSERT INTO Producto (nombre, descripcion, precioUnitario, stock, proveedor_id) VALUES 
('Detox Verde', 'Jugo de espinaca...', 2.50, 50, 1), -- 1 = Frutas del Huerto
('Energía Tropical', 'Smoothie de mango...', 3.00, 40, 1), -- 1 = Frutas del Huerto
('Vitamina C Plus', 'Extracto de naranja...', 2.75, 35, 2); -- 2 = AgroDistribuidora




