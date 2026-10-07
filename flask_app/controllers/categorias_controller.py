from flask import Blueprint, render_template, redirect, request, session
from flask_app.models.categoria import Categoria

categorias_bp = Blueprint('categorias', __name__)

# Vista del listado (Para mostrar todas las categorías junto con el conteo de tareas del usuario)
@categorias_bp.route('/categorias')
def ver_categorias():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    lista_categorias = Categoria.leer_con_conteo_usuario(session['usuario_id'])
    return render_template('categorias.html', categorias=lista_categorias)

# Vista de creación (Para mostrar el formulario de registro de una nueva categoría)
@categorias_bp.route('/categorias/nueva')
def vista_nueva_categoria():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    return render_template('nueva_categoria.html')

# Vista de detalle (Para desplegar la información y total de tareas de una categoría específica)
@categorias_bp.route('/categorias/<int:id_categoria>')
def ver_detalle_categoria(id_categoria):
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    
    categoria_individual = Categoria.obtener_por_id_con_conteo(id_categoria)
    if not categoria_individual:
        return redirect('/categorias')
        
    return render_template('ver_categoria.html', categoria=categoria_individual)

# Acción POST (Para validar y guardar un nuevo registro de categoría en la base de datos)
@categorias_bp.route('/categorias/crear', methods=['POST'])
def crear():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')

    if not Categoria.validar_categoria(request.form):
        return redirect('/categorias/nueva')
        
    data = {
        "nombre": request.form['nombre'],
        "descripcion": request.form['descripcion'],
        "usuario_id": session['usuario_id']
    }
    Categoria.crear_categoria(data)
    return redirect('/categorias')

# Vista de edición (Para recuperar los datos actuales de la categoría y cargarlos en el formulario)
@categorias_bp.route('/categorias/editar/<int:id_categoria>')
def vista_editar_categoria(id_categoria):
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    
    categoria_individual = Categoria.obtener_por_id(id_categoria)
    if not categoria_individual:
        return redirect('/categorias')
        
    return render_template('editar_categoria.html', categoria=categoria_individual)

# Acción POST (Para validar y sobreescribir los datos modificados de una categoría existente)
@categorias_bp.route('/categorias/actualizar', methods=['POST'])
def actualizar():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    if not Categoria.validar_categoria(request.form):
        return redirect(f"/categorias/editar/{request.form['id_categoria']}")
    Categoria.actualizar_categoria(request.form)
    return redirect('/categorias')

# Acción de actualización de borrado (Borrado lógico para cambiar el estado activo a oculto)
@categorias_bp.route('/categorias/borrar/<int:id_categoria>')
def borrar(id_categoria):
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    Categoria.borrar_categoria(id_categoria)
    return redirect('/categorias')
