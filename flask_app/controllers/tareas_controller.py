from flask import Blueprint, render_template, redirect, request, session
from flask_app.models.tarea import Tarea
from flask_app.models.categoria import Categoria 

tareas_bp = Blueprint('tareas', __name__)

# Vista del panel (Para listar, buscar y filtrar todas las tareas activas)
@tareas_bp.route('/tareas')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
        
    busqueda = request.args.get('buscar', '').strip().lower()
    cat_filtro = request.args.get('categoria', 'todos')
    pri_filtro = request.args.get('prioridad', 'todos')
    est_filtro = request.args.get('estado', 'todos')
    
    tareas_filtradas = Tarea.obtener_todo()
    lista_categorias = Categoria.read_all() if hasattr(Categoria, 'read_all') else Categoria.leer_todas()
    
    if busqueda:
        tareas_filtradas = [t for t in tareas_filtradas if busqueda in t.titulo.lower()]
        
    if cat_filtro != 'todos':
        tareas_filtradas = [t for t in tareas_filtradas if str(t.categoria) == str(cat_filtro)]
        
    if pri_filtro != 'todos':
        tareas_filtradas = [t for t in tareas_filtradas if t.nombre_prioridad == pri_filtro]
        
    if est_filtro != 'todos':
        tareas_filtradas = [t for t in tareas_filtradas if t.nombre_estado == est_filtro]

    return render_template(
        'tareas.html', 
        tareas=tareas_filtradas, 
        categorias=lista_categorias,
        buscar_sel=busqueda,
        categoria_sel=cat_filtro,
        prioridad_sel=pri_filtro,
        estado_sel=est_filtro
    )

# Vista de creación (Para mostrar el formulario de registro de una nueva tarea)
@tareas_bp.route('/tareas/nueva')
def vista_nueva_tarea():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    lista_categorias = Categoria.read_all() if hasattr(Categoria, 'read_all') else Categoria.leer_todas()
    return render_template('nueva_tarea.html', categorias=lista_categorias)

# Vista de detalle (Para desplegar toda la información individual de una tarea específica)
@tareas_bp.route('/tareas/<int:id_tarea>')
def ver_detalle_tarea(id_tarea):
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
        
    tarea_individual = Tarea.obtener_tarea_por_id(id_tarea)
    if not tarea_individual:
        return redirect('/tareas')
        
    return render_template('ver_tarea.html', tarea=tarea_individual)

# Acción de actualización rápida (Para cambiar el estado de la tarea directamente a completada)
@tareas_bp.route('/tareas/completar/<int:id_tarea>')
def completar_tarea(id_tarea):
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
        
    Tarea.marcar_completada(id_tarea)
    return redirect('/tareas')

# Acción de actualización rápida (Para revertir el estado de una tarea completada a en progreso)
@tareas_bp.route('/tareas/desmarcar/<int:id_tarea>')
def desmarcar_tarea(id_tarea):
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
        
    Tarea.desmarcar_completada(id_tarea)
    return redirect('/tareas')

# Acción POST (Para validar y guardar un nuevo registro de tarea en la base de datos)
@tareas_bp.route('/tareas/registrar', methods=['POST'])
def registrar_tarea():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    if not Tarea.validar_tarea(request.form):
        return redirect('/tareas/nueva')
    data = {
        "titulo": request.form['titulo'],
        "categoria": request.form['categoria'],
        "prioridad": request.form['prioridad'],
        "estado": request.form['estado'],
        "fecha_limite": request.form['fecha_limite'],
        "descripcion": request.form.get('descripcion', ''),
        "usuario_id": session['usuario_id'],
        "created_by": session['usuario_id']
    }
    Tarea.registrar_tarea(data)
    return redirect('/tareas')

# Vista de edición (Para recuperar los datos actuales de la tarea y cargarlos en el formulario)
@tareas_bp.route('/tareas/editar/<int:id_tarea>')
def vista_editar_tarea(id_tarea):
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    tarea_individual = Tarea.obtener_tarea_por_id(id_tarea)
    lista_categorias = Categoria.read_all() if hasattr(Categoria, 'read_all') else Categoria.leer_todas()
    return render_template('editar_tarea.html', tarea=tarea_individual, categories=lista_categorias, categorias=lista_categorias)

# Acción POST (Para validar y sobreescribir los datos modificados de una tarea existente)
@tareas_bp.route('/tareas/actualizar', methods=['POST'])
def actualizar_tarea():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    if not Tarea.validar_tarea(request.form):
        return redirect(f"/tareas/editar/{request.form['id_tarea']}")
    data = {
        "id_tarea": request.form['id_tarea'],
        "titulo": request.form['titulo'],
        "categoria": request.form['categoria'],
        "prioridad": request.form['prioridad'],
        "estado": request.form['estado'],
        "fecha_limite": request.form['fecha_limite'],
        "descripcion": request.form.get('descripcion', ''),
        "updated_by": session['usuario_id']
    }
    Tarea.actualizar_tarea(data)
    return redirect('/tareas')

# Acción de actualización de borrado (Borrado lógico para cambiar el estado activo a oculto)
@tareas_bp.route('/tareas/eliminar/<int:id_tarea>')
def eliminar(id_tarea):
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    Tarea.eliminar_tarea(id_tarea)
    return redirect('/tareas')
