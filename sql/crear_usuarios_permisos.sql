-- Creamos el usuario del administrador
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON bd_frutalizate.* TO 'admin'@'localhost' WITH GRANT OPTION;

-- desarrollador, maneja estructur y datos pero no puede borrar la BD
CREATE USER IF NOT EXISTS 'desarrollador'@'localhost' IDENTIFIED BY 'desarrollador';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER ON bd_frutalizate.* TO 'desarrollador'@'localhost';

-- Usuario servicio,  manipula datos y ejecuta funciones/procedimientos
CREATE USER IF NOT EXISTS 'servicios'@'localhost' IDENTIFIED BY 'servicios';
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON bd_frutalizate.* TO 'servicios'@'localhost';

-- Analista/reportes, solo lectura para las Vistas
CREATE USER IF NOT EXISTS 'analista'@'localhost' IDENTIFIED BY 'analista';
GRANT SELECT ON bd_frutalizate.* TO 'analista'@'localhost';


-- Cajero, Puede ver productos y registrar ventas, pero NO puede borrar registros ni alterar tablas.
CREATE USER IF NOT EXISTS 'cajero'@'localhost' IDENTIFIED BY 'cajero';
GRANT SELECT, INSERT, UPDATE ON bd_frutalizate.pedido TO 'cajero'@'localhost';
GRANT SELECT ON bd_frutalizate.producto TO 'cajero'@'localhost';
GRANT SELECT ON bd_frutalizate.cliente TO 'cajero'@'localhost';

-- Aplicar los cambios
FLUSH PRIVILEGES;

