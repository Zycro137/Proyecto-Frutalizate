CREATE DATABASE IF NOT EXISTS bd_frutalizate;
USE bd_frutalizate;

CREATE TABLE IF NOT EXISTS Proveedor (
    proveedor_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    telefono VARCHAR(255),
    direccion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Frutas (
    frutas_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    stock int NOT NULL,
	proveedor_id INT,
    FOREIGN KEY (proveedor_id) REFERENCES Proveedor(proveedor_id)
);

CREATE TABLE IF NOT EXISTS Producto (
    producto_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255),
    precioUnitario FLOAT NOT NULL,
    stock INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Producto_Fruta (
    producto_id INT,
    frutas_id INT,
    PRIMARY KEY (producto_id, frutas_id),
    FOREIGN KEY (producto_id) REFERENCES Producto(producto_id),
    FOREIGN KEY (frutas_id) REFERENCES Frutas(frutas_id)
);


CREATE TABLE IF NOT EXISTS Cliente (
    cliente_id VARCHAR(255) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    telefono VARCHAR(255),
    dirección VARCHAR(255),
    email VARCHAR(255)
);



CREATE TABLE IF NOT EXISTS Suscripcion (
	suscripcion_id INT AUTO_INCREMENT PRIMARY KEY,
    frecuencia INT,
    fecha_inicio DATE,
    fecha_proxEntrega DATE,
    estado VARCHAR(255),
    cliente_id VARCHAR(255),
    CONSTRAINT FK_Suscripcion_Cliente
    FOREIGN KEY (cliente_id) REFERENCES Cliente(cliente_id)
);

CREATE TABLE IF NOT EXISTS Suscripcion_Detalle (
    susDetalle_id INT AUTO_INCREMENT PRIMARY KEY,
    cantidad INT NOT NULL,
    subtotal FLOAT,
    producto_id INT,
    suscripcion_id INT,
    FOREIGN KEY (producto_id) REFERENCES Producto(producto_id),
    FOREIGN KEY (suscripcion_id) REFERENCES Suscripcion(suscripcion_id)
);


CREATE TABLE IF NOT EXISTS Repartidor (
    repartidor_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    telefono VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Pedido (
    pedido_id INT AUTO_INCREMENT PRIMARY KEY,
    fechaRealizado DATE,
    estado VARCHAR(255),
    total FLOAT,
    cliente_id VARCHAR(255),
    repartidor_id INT,
    suscripcion_id INT, -- Puede ser NULL si es una compra única
    FOREIGN KEY (cliente_id) REFERENCES Cliente(cliente_id),
    FOREIGN KEY (repartidor_id) REFERENCES Repartidor(repartidor_id),
    FOREIGN KEY (suscripcion_id) REFERENCES Suscripcion(suscripcion_id)
);

CREATE TABLE IF NOT EXISTS Detalle_Pedido (
    pediDetalle_id INT AUTO_INCREMENT PRIMARY KEY,
    cantidad INT NOT NULL,
    subtotal FLOAT,
    pedido_id INT,
    producto_id INT,
    FOREIGN KEY (pedido_id) REFERENCES Pedido(pedido_id),
    FOREIGN KEY (producto_id) REFERENCES Producto(producto_id)
);


CREATE TABLE IF NOT EXISTS Entrega (
    entrega_id INT AUTO_INCREMENT PRIMARY KEY,
    fechaEntrega DATE,
    estadoEntrega VARCHAR(255),
    pedido_id INT UNIQUE,
    FOREIGN KEY (pedido_id) REFERENCES Pedido(pedido_id)
);
