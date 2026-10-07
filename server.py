from flask_app import app
from flask_app.controllers.usuarios_controller import usuarios_bp
from flask_app.controllers.categorias_controller import categorias_bp
from flask_app.controllers.tareas_controller import tareas_bp

# Blueprints
app.register_blueprint(usuarios_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(tareas_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
