import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Clave secreta para sesiones y formularios
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'carflix-secret-key-super-segura-2024'

    # Configuración de la base de datos SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'carflix.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de uploads
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB máximo por archivo

    # Extensiones permitidas
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mkv', 'mov'}
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}