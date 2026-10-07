from datetime import datetime
from flask import flash
from flask_app.config.pymysqlconnection import connectToMySQL

class Tarea:
    DB = 'esquema_tasktrack'
    def __init__(self, data):
        # Datos de control
        self.id_tarea = data.get('id_tarea')
        self.titulo = data.get('titulo')
        self.fecha_limite = data.get('fecha_limite')
        self.fecha_creacion = data.get('created_at')
        self.categoria = data.get('categoria')
        self.prioridad = data.get('prioridad')
        self.estado = data.get('estado')
        self.usuario = data.get('usuario')
        self.descripcion = data.get('descripcion')
        # Datos de visualisación (para los Join)
        self.nombre_categoria = data.get('categoria_nombre')
        self.nombre_prioridad = data.get('prioridad_nombre')
        self.nombre_estado = data.get('estado_nombre')
        self.dias_restantes = self.calcular_dias()

    # Lógica detras del calculo de días restantes
    def calcular_dias(self):
        if not self.fecha_limite:
            return "N/A"
        try:
            hoy = datetime.now().date()
            if isinstance(self.fecha_limite, str):
                limite = datetime.strptime(self.fecha_limite, '%Y-%m-%d').date()
            else:
                limite = self.fecha_limite
            diff = (limite - hoy).days
            if diff < 0:
                return "Vencida"
            elif diff == 0:
                return "Hoy"
            return f"{diff} días"
        except:
            return "N/A"

    # Read (Para listar todas las tareas con sus relaciones asociadas)
    @classmethod
    def obtener_todo(cls):
        query = """
            SELECT 
                t.*, 
                c.nombre AS categoria_nombre, 
                p.nombre AS prioridad_nombre, 
                e.nombre AS estado_nombre
            FROM tareas t
            INNER JOIN categorias c ON t.categoria = c.id_categoria
            INNER JOIN prioridades p ON t.prioridad = p.id_prioridad
            INNER JOIN estados e ON t.estado = e.id_estado
            WHERE t.deleted = 0;
        """
        resultados_bd = connectToMySQL(cls.DB).query_db(query)
        if not resultados_bd:
            return []
        return [cls(fila) for fila in resultados_bd]

    # Create (Para insertar una nueva tarea en la base de datos)
    @classmethod
    def registrar_tarea(cls, formulario):
        query = """
            INSERT INTO tareas (titulo, categoria, prioridad, estado, fecha_limite, descripcion, usuario, created_by)
            VALUES (%(titulo)s, %(categoria)s, %(prioridad)s, %(estado)s, %(fecha_limite)s, %(descripcion)s, %(usuario_id)s, %(created_by)s);
        """
        return connectToMySQL(cls.DB).query_db(query, formulario)

    # Read por ID (Para buscar y desplegar la información de una tarea específica)
    @classmethod
    def obtener_tarea_por_id(cls, id_tarea):
        query = """
            SELECT 
                t.*, 
                c.nombre AS categoria_nombre, 
                p.nombre AS prioridad_nombre, 
                e.nombre AS estado_nombre
            FROM tareas t
            INNER JOIN categorias c ON t.categoria = c.id_categoria
            INNER JOIN prioridades p ON t.prioridad = p.id_prioridad
            INNER JOIN estados e ON t.estado = e.id_estado
            WHERE t.id_tarea = %(id_tarea)s AND t.deleted = 0;
        """
        data = {'id_tarea': id_tarea}
        resultados_bd = connectToMySQL(cls.DB).query_db(query, data)
        if not resultados_bd:
            return None
        return cls(resultados_bd[0])

    # Update (Para modificar los campos principales de una tarea existente)
    @classmethod
    def actualizar_tarea(cls, formulario):
        query = """
            UPDATE tareas 
            SET titulo = %(titulo)s, categoria = %(categoria)s, prioridad = %(prioridad)s, 
                estado = %(estado)s, fecha_limite = %(fecha_limite)s, descripcion = %(descripcion)s, updated_by = %(updated_by)s
            WHERE id_tarea = %(id_tarea)s;
        """
        return connectToMySQL(cls.DB).query_db(query, formulario)

    # Update de Estado (Para cambiar directamente el estado de una tarea a Completada)
    @classmethod
    def marcar_completada(cls, id_tarea):
        query = """
            UPDATE tareas 
            SET estado = 3 
            WHERE id_tarea = %(id_tarea)s;
        """
        data = {'id_tarea': id_tarea}
        return connectToMySQL(cls.DB).query_db(query, data)

    # Update de Estado (Para revertir el estado de una tarea a En Progreso)
    @classmethod
    def desmarcar_completada(cls, id_tarea):
        query = """
            UPDATE tareas 
            SET estado = 2 
            WHERE id_tarea = %(id_tarea)s;
        """
        data = {'id_tarea': id_tarea}
        return connectToMySQL(cls.DB).query_db(query, data)

    # Delete (Borrado lógico para ocultar la tarea cambiando la bandera deleted)
    @classmethod
    def eliminar_tarea(cls, id_tarea):
        query = """
            UPDATE tareas 
            SET deleted = 1 
            WHERE id_tarea = %(id_tarea)s;
        """
        data = {'id_tarea': id_tarea}
        return connectToMySQL(cls.DB).query_db(query, data)

    # Validaciones (Verificaciones lógicas de campos obligatorios en el formulario)
    @classmethod
    def validar_tarea(cls, formulario):
        es_valido = True
        if len(formulario.get('titulo', '').strip()) < 3:
            flash("El título de la tarea debe tener al menos 3 caracteres.", "tarea")
            es_valido = False
        if not formulario.get('categoria'):
            flash("Debes seleccionar una categoría para la tarea.", "tarea")
            es_valido = False
        if not formulario.get('prioridad'):
            flash("Debes asignar una prioridad a la tarea.", "tarea")
            es_valido = False
        if not formulario.get('fecha_limite'):
            flash("Debes ingresar una fecha límite para la tarea.", "tarea")
            es_valido = False
        return es_valido
