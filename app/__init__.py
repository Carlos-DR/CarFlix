from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Inicialización de extensiones
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

    # Importar modelos y rutas dentro de la función para evitar importaciones circulares
    with app.app_context():
        from app import routes, models

        # Crear las tablas de la base de datos
        db.create_all()

        # Crear usuario administrador por defecto si no existe
        from app.models import User
        admin = User.query.filter_by(email='admin@carflix.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@carflix.com',
                is_admin=True
            )
            admin.set_password('admin123')  # Contraseña por defecto
            db.session.add(admin)
            db.session.commit()
            print("✓ Usuario administrador creado: admin@carflix.com / admin123")

    return app