-- Base de Datos para TaskTrack App Flask
CREATE DATABASE IF NOT EXISTS esquema_tasktrack;
USE esquema_tasktrack;

-- Tabla "usuarios"
CREATE TABLE IF NOT EXISTS usuarios (
	id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(200) NOT NULL,
    contrasena VARCHAR(225) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) NOT NULL DEFAULT 0
);

-- Tabla "categorias"
CREATE TABLE IF NOT EXISTS categorias (
	id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(300) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) NOT NULL DEFAULT 0
);

-- Tabla "prioridades"
CREATE TABLE IF NOT EXISTS prioridades (
	id_prioridad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(300) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) NOT NULL DEFAULT 0
);

-- Tabla "estados"
CREATE TABLE IF NOT EXISTS estados (
	id_estado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(300) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) NOT NULL DEFAULT 0
);

-- Tabla "tareas"
CREATE TABLE IF NOT EXISTS tareas (
	id_tarea INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(50) NOT NULL,
    categoria INT NOT NULL,
    prioridad INT NOT NULL,
    estado INT NOT NULL,
    fecha_limite DATE NOT NULL,
    descripcion VARCHAR(500) NOT NULL,
    usuario INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) NOT NULL DEFAULT 0,
    FOREIGN KEY (categoria) REFERENCES categorias(id_categoria) ON DELETE RESTRICT,
    FOREIGN KEY (prioridad) REFERENCES prioridades(id_prioridad) ON DELETE RESTRICT,
    FOREIGN KEY (estado) REFERENCES estados(id_estado) ON DELETE RESTRICT,
    FOREIGN KEY (usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT
);
