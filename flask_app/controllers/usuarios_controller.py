from flask import Blueprint, render_template, redirect, request, session, flash
from flask_app.models.usuario import Usuario
from flask_app import bcrypt

usuarios_bp = Blueprint('usuarios', __name__)

# Vista principal (Para redirigir al dashboard o mostrar el formulario de registro)
@usuarios_bp.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/tareas')
    return render_template('registrarse.html')

# Vista de autenticación (Para mostrar el formulario de inicio de sesión)
@usuarios_bp.route('/iniciar-sesion')
def vista_login():
    if 'usuario_id' in session:
        return redirect('/tareas')
    return render_template('iniciar_sesion.html')

# Acción POST (Para procesar el registro de un nuevo usuario con contraseña encriptada)
@usuarios_bp.route('/usuarios/registrar', methods=['POST'])
def procesar_registro():
    if not Usuario.validar_registro(request.form):
        return redirect('/')

    if request.form.get('contrasena') != request.form.get('confirmar_contrasena'):
        flash("Las contraseñas no coinciden.", "registro")
        return redirect('/')

    password_encriptada = bcrypt.generate_password_hash(request.form['contrasena']).decode('utf-8')
    
    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "contrasena": password_encriptada
    }
    
    usuario_id = Usuario.guardar_usuario(data)
    session['usuario_id'] = usuario_id
    session['usuario_nombre'] = f"{data['nombre']} {data['apellido']}"
    
    return redirect('/tareas')

# Acción POST (Para verificar las credenciales del usuario e iniciar sesión)
@usuarios_bp.route('/usuarios/login', methods=['POST'])
def procesar_login():
    usuario = Usuario.obtener_por_email(request.form['email'])
    
    if not usuario or not bcrypt.check_password_hash(usuario.contrasena, request.form['contrasena']):
        flash("Credenciales incorrectas.", "danger")
        return redirect('/iniciar-sesion')

    session['usuario_id'] = usuario.id_usuario
    session['usuario_nombre'] = f"{usuario.nombre} {usuario.apellido}"
    return redirect('/tareas')

# Vista de salida (Para limpiar las variables de sesión activa y redirigir al login)
@usuarios_bp.route('/usuarios/logout')
def logout():
    session.clear()
    return redirect('/iniciar-sesion')
