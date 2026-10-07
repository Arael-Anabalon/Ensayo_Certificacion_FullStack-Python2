import re
from flask import flash
from flask_app.config.pymysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    DB = 'esquema_tasktrack'
    def __init__(self, data):
        # Datos de control
        self.id_usuario = data.get('id_usuario')
        self.nombre = data.get('nombre')
        self.apellido = data.get('apellido')
        self.email = data.get('email')
        self.contrasena = data.get('contrasena')

    # Create (Para registrar un nuevo usuario en el sistema)
    @classmethod
    def guardar_usuario(cls, formulario):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, contrasena)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(contrasena)s);
        """
        return connectToMySQL(cls.DB).query_db(query, formulario)
    
    # Read por ID (Para buscar y obtener los datos de un usuario específico)
    @classmethod
    def ver_usuario(cls, id_usuario):
        query = "SELECT * FROM usuarios WHERE id_usuario = %(id_usuario)s AND deleted = 0;"
        data = {'id_usuario': id_usuario}
        resultado = connectToMySQL(cls.DB).query_db(query, data)
        if not resultado:
            return None
        return cls(resultado[0])

    # Read por email (Para buscar las credenciales de un usuario durante el login)
    @classmethod
    def obtener_por_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s AND deleted = 0;"
        data = {'email': email}
        resultado = connectToMySQL(cls.DB).query_db(query, data)
        if not resultado:
            return None
        return cls(resultado[0])

    # Update (Para modificar la información de perfil de un usuario existente)
    @classmethod
    def actualizar_usuario(cls, formulario):
        query = """
            UPDATE usuarios 
            SET nombre = %(nombre)s, apellido = %(apellido)s, email = %(email)s
            WHERE id_usuario = %(id_usuario)s;
        """
        return connectToMySQL(cls.DB).query_db(query, formulario)
    
    # Delete (Borrado lógico para desactivar la cuenta cambiando la bandera deleted)
    @classmethod
    def borrar_usuario(cls, id_usuario):
        query = "UPDATE usuarios SET deleted = 1 WHERE id_usuario = %(id_usuario)s;"
        data = {'id_usuario': id_usuario}
        return connectToMySQL(cls.DB).query_db(query, data)

    # Validaciones (Verificaciones lógicas de campos obligatorios y correo único)
    @classmethod
    def validar_registro(cls, formulario):
        es_valido = True

        if len(formulario.get('nombre', '').strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            es_valido = False

        if not EMAIL_REGEX.match(formulario.get('email', '')):
            flash("La dirección de correo electrónico es inválida.", "registro")
            es_valido = False

        query = "SELECT * FROM usuarios WHERE email = %(email)s AND deleted = 0;"
        resultados = connectToMySQL(cls.DB).query_db(query, formulario)
        if resultados:
            flash("Este correo electrónico ya está registrado.", "registro")
            es_valido = False

        return es_valido
