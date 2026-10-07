from flask_app.config.pymysqlconnection import connectToMySQL
from flask import flash

class Categoria:
    DB = 'esquema_tasktrack'
    def __init__(self, data):
        # Datos de control
        self.id_categoria = data.get('id_categoria')
        self.nombre = data.get('nombre')
        self.descripcion = data.get('descripcion')
        # Datos de visualisación
        self.cantidad_tareas = data.get('cantidad_tareas')
        self.fecha_creacion = data.get('created_at')

    # Create (Para insertar una nueva categoría en la base de datos)
    @classmethod
    def crear_categoria(cls, formulario):
        query = """
            INSERT INTO categorias (nombre, descripcion, created_by) 
            VALUES (%(nombre)s, %(descripcion)s, %(usuario_id)s);
        """
        return connectToMySQL(cls.DB).query_db(query, formulario)

    # Read (Para listar categorías incluyendo la cantidad de tareas del usuario actual)
    @classmethod
    def leer_con_conteo_usuario(cls, id_usuario):
        query = """
            SELECT c.*, COUNT(t.id_tarea) AS cantidad_tareas
            FROM categorias c
            LEFT JOIN tareas t ON c.id_categoria = t.categoria AND t.usuario = %(id_usuario)s AND t.deleted = 0
            WHERE c.deleted = 0
            GROUP BY c.id_categoria;
        """
        data = {'id_usuario': id_usuario}
        resultados = connectToMySQL(cls.DB).query_db(query, data)
        return [cls(row) for row in resultados] if resultados else []

    # Read (Para rellenar menús desplegables <select> en los formularios de tareas)
    @classmethod
    def leer_todas(cls):
        query = "SELECT * FROM categorias WHERE deleted = 0;"
        resultados = connectToMySQL(cls.DB).query_db(query)
        return [cls(row) for row in resultados] if resultados else []

    # Read por ID (Para ver el detalle de una categoría junto al total de tareas asociadas)
    @classmethod
    def obtener_por_id_con_conteo(cls, id_categoria):
        query = """
            SELECT c.*, COUNT(t.id_tarea) AS cantidad_tareas
            FROM categorias c
            LEFT JOIN tareas t ON c.id_categoria = t.categoria AND t.deleted = 0
            WHERE c.id_categoria = %(id_categoria)s AND c.deleted = 0
            GROUP BY c.id_categoria;
        """
        data = {'id_categoria': id_categoria}
        resultados = connectToMySQL(cls.DB).query_db(query, data)
        if not resultados:
            return None
        return cls(resultados[0])

    # Read por ID (Para recuperar los datos limpios de una categoría específica)
    @classmethod
    def obtener_por_id(cls, id_categoria):
        query = "SELECT * FROM categorias WHERE id_categoria = %(id_categoria)s AND deleted = 0;"
        data = {'id_categoria': id_categoria}
        resultados = connectToMySQL(cls.DB).query_db(query, data)
        if not resultados:
            return None
        return cls(resultados[0])

    # Update (Para modificar los campos principales de una categoría existente)
    @classmethod
    def actualizar_categoria(cls, formulario):
        query = """
            UPDATE categorias 
            SET nombre = %(nombre)s, descripcion = %(descripcion)s 
            WHERE id_categoria = %(id_categoria)s;
        """
        return connectToMySQL(cls.DB).query_db(query, formulario)

    # Delete (Borrado lógico para ocultar la categoría cambiando la bandera deleted)
    @classmethod 
    def borrar_categoria(cls, id_categoria):
        query = "UPDATE categorias SET deleted = 1 WHERE id_categoria = %(id_categoria)s;"
        data = {'id_categoria': id_categoria}
        return connectToMySQL(cls.DB).query_db(query, data)

    # Validaciones (Verificaciones lógicas de longitud para los campos obligatorios)
    @staticmethod
    def validar_categoria(formulario):
        es_valido = True
        if len(formulario.get('nombre', '').strip()) < 3:
            flash("El nombre de la categoría debe tener al menos 3 caracteres.", "categoria")
            es_valido = False     
        if len(formulario.get('descripcion', '').strip()) < 5:
            flash("La descripción debe tener al menos 5 caracteres.", "categoria")
            es_valido = False
        return es_valido
