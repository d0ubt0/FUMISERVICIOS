-- SCRIPT DEDICADO A LA CREACION DE LA BASE DE DATOS DE FUMISERVICIOS.
-- by: Jhofred por si me quieren putear

-- DROP DATABASE fumiservicios.db;
-- CREATE DATABASE fumiservicios; (NO FUNCIONA NI IDEA PORQUE)

-- Usuario

CREATE TABLE Usuario(
	id INTEGER PRIMARY KEY,
	nombre TEXT NOT NULL,
	email TEXT NOT NULL,
	contrasena TEXT NOT NULL,
	tipo TEXT NOT NULL,
	CHECK(tipo in('CTecnico', 'TEspecializado', 'ACliente', 'EqTecnico')),
    UNIQUE(email)
	);

-- DATOS DE PRUEBA USUARIO:

/*
SELECT * FROM Usuario;

-- INSERT INTO Usuario (nombre, email, contrasena, tipo)
	VALUES 
	('Jhofred', 'jhofred@gmail.com', 'jhofred123', 'EqTecnico'),
	('papisam', 'papisam@gmail.com', 'papisam123', 'CTecnico');
*/

-- CLIENTE

CREATE TABLE Cliente(
	id INTEGER PRIMARY KEY,
	nombre TEXT NOT NULL,
	telefono INTEGER NOT NULL,
	email TEXT,
    UNIQUE(email),
    UNIQUE(telefono)
);

-- SELECT * FROM Cliente;

-- SOLICITUD

CREATE TABLE Solicitud(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_cliente INTEGER NOT NULL,
	id_usuario INTEGER NOT NULL,
	descripcion TEXT NOT NULL,
	tipo_servicio TEXT NOT NULL,
	direccion TEXT NOT NULL,
	FOREIGN KEY(id_cliente) REFERENCES Cliente(id),
	FOREIGN KEY(id_usuario) REFERENCES Usuario(id)
);

-- AGENDA

CREATE TABLE Agenda(
	id INTEGER PRIMARY KEY,
	id_usuario INTEGER NOT NULL,
	fecha DATE NOT NULL,
	tipo_actividad TEXT NOT NULL,
	CHECK(tipo_actividad in ('diagnostico','servicio')),
	FOREIGN KEY(id_usuario) REFERENCES Usuario(id)
);

-- INSERTS PARA LA TABLA Usuario
INSERT INTO Usuario (nombre, email, contrasena, tipo)
VALUES 
('Carlos Pérez', 'carlos.perez@gmail.com', 'securePass1', 'CTecnico'),
('María González', 'maria.gonzalez@gmail.com', 'pass4Maria', 'TEspecializado'),
('Andrea Ruiz', 'andrea.ruiz@gmail.com', 'andyPassword5', 'ACliente');

-- INSERTS PARA LA TABLA Cliente
INSERT INTO Cliente (nombre, telefono, email)
VALUES 
('Juan Gómez', 1234567890, 'juan.gomez@gmail.com'),
('Ana López', 9876543210, 'ana.lopez@gmail.com'),
('Pedro Castillo', 1122334455, 'pedro.castillo@gmail.com');

-- INSERTS PARA LA TABLA Solicitud
INSERT INTO Solicitud (id_cliente, id_usuario, descripcion, tipo_servicio, direccion)
VALUES 
(1, 1, 'Fumigación de control básico en apartamento', 'fumigación', 'Calle 1 #10-20'),
(2, 2, 'Diagnóstico preliminar de plaga en oficina', 'diagnóstico', 'Avenida 5 #30-45'),
(3, 3, 'Control especializado de plagas en restaurante', 'fumigación', 'Carrera 7 #50-60');

-- INSERTS PARA LA TABLA Agenda
INSERT INTO Agenda (id, id_usuario, fecha, tipo_actividad)
VALUES 
(1, 1, '2025-02-10', 'diagnostico'),
(2, 2, '2025-02-15', 'servicio'),
(3, 3, '2025-02-20', 'diagnostico');


SELECT * FROM Usuario;
SELECT * FROM Cliente;
SELECT * FROM Solicitud;
SELECT * FROM Agenda;



-- !!!!
-- ELIMINAR CADA TABLA:
-- DROP TABLE Agenda;
-- DROP TABLE Solicitud;
-- DROP TABLE Cliente;
-- DROP TABLE Usuario;