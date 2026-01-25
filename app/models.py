from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

# Tabla de relación muchos a muchos: Películas-Categorías
movie_categories = db.Table('movie_categories',
                            db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
                            db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
                            )

# Tabla de relación muchos a muchos: Series-Categorías
series_categories = db.Table('series_categories',
                             db.Column('series_id', db.Integer, db.ForeignKey('series.id'), primary_key=True),
                             db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
                             )

# Tabla de favoritos de películas
movie_favorites = db.Table('movie_favorites',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                           db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
                           db.Column('added_date', db.DateTime, default=datetime.utcnow)
                           )

# Tabla de favoritos de series
series_favorites = db.Table('series_favorites',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                            db.Column('series_id', db.Integer, db.ForeignKey('series.id'), primary_key=True),
                            db.Column('added_date', db.DateTime, default=datetime.utcnow)
                            )

# Tabla de películas vistas
movie_watched = db.Table('movie_watched',
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                         db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
                         db.Column('watched_date', db.DateTime, default=datetime.utcnow)
                         )

# Tabla de episodios vistos
episode_watched = db.Table('episode_watched',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                           db.Column('episode_id', db.Integer, db.ForeignKey('episode.id'), primary_key=True),
                           db.Column('watched_date', db.DateTime, default=datetime.utcnow)
                           )


class User(UserMixin, db.Model):
    """Modelo de Usuario"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    profile_picture = db.Column(db.String(300), default='images/default-avatar.png')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    favorite_movies = db.relationship('Movie', secondary=movie_favorites,
                                      backref=db.backref('favorited_by', lazy='dynamic'))
    favorite_series = db.relationship('Series', secondary=series_favorites,
                                      backref=db.backref('favorited_by', lazy='dynamic'))
    watched_movies = db.relationship('Movie', secondary=movie_watched,
                                     backref=db.backref('watched_by', lazy='dynamic'))
    watched_episodes = db.relationship('Episode', secondary=episode_watched,
                                       backref=db.backref('watched_by', lazy='dynamic'))

    def set_password(self, password):
        """Establece la contraseña hasheada"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    """Modelo de Categoría/Género"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'


class Movie(db.Model):
    """Modelo de Película"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)  # Duración en minutos
    release_year = db.Column(db.Integer)
    video_path = db.Column(db.String(300), nullable=False)
    poster_path = db.Column(db.String(300))
    background_path = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    categories = db.relationship('Category', secondary=movie_categories,
                                 backref=db.backref('movies', lazy='dynamic'))

    def __repr__(self):
        return f'<Movie {self.title}>'


class Series(db.Model):
    """Modelo de Serie"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    release_year = db.Column(db.Integer)
    poster_path = db.Column(db.String(300))
    background_path = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    categories = db.relationship('Category', secondary=series_categories,
                                 backref=db.backref('series', lazy='dynamic'))
    episodes = db.relationship('Episode', backref='series', lazy='dynamic',
                               cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Series {self.title}>'


class Episode(db.Model):
    """Modelo de Episodio"""
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=False)
    season_number = db.Column(db.Integer, nullable=False)
    episode_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)  # Duración en minutos
    video_path = db.Column(db.String(300), nullable=False)
    thumbnail_path = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Episode S{self.season_number}E{self.episode_number}: {self.title}>'


@login_manager.user_loader
def load_user(user_id):
    """Carga el usuario para Flask-Login"""
    return User.query.get(int(user_id))