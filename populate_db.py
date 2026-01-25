"""
Script para poblar la base de datos de Carflix con datos de prueba
Ejecutar: python populate_db.py
"""

from app import create_app, db
from app.models import User, Movie, Series, Episode, Category
from datetime import datetime
import os

def populate_categories():
    """Crear categorías"""
    categories_data = [
        'Acción', 'Aventura', 'Comedia', 'Drama', 'Ciencia Ficción',
        'Terror', 'Thriller', 'Romance', 'Animación', 'Documental',
        'Fantasía', 'Musical', 'Crimen', 'Misterio', 'Familiar'
    ]

    categories = []
    for cat_name in categories_data:
        cat = Category.query.filter_by(name=cat_name).first()
        if not cat:
            cat = Category(name=cat_name)
            db.session.add(cat)
            categories.append(cat)
            print(f"✓ Categoría creada: {cat_name}")
        else:
            categories.append(cat)

    db.session.commit()
    return categories


def populate_movies(categories):
    """Crear películas de ejemplo"""
    movies_data = [
        {
            'title': 'El Gran Escape',
            'description': 'Una emocionante historia de aventura y supervivencia en la que un grupo de amigos debe escapar de una isla desierta tras un naufragio. Llena de acción, humor y momentos emotivos.',
            'duration': 128,
            'release_year': 2023,
            'categories': ['Acción', 'Aventura']
        },
        {
            'title': 'Risas en la Ciudad',
            'description': 'Comedia romántica sobre dos desconocidos que se conocen en el metro y viven una serie de situaciones hilarantes mientras intentan llegar a una cita importante.',
            'duration': 95,
            'release_year': 2024,
            'categories': ['Comedia', 'Romance']
        },
        {
            'title': 'Dimensión X',
            'description': 'Thriller de ciencia ficción que explora los peligros de la tecnología de realidad virtual cuando un científico queda atrapado en su propia creación.',
            'duration': 142,
            'release_year': 2023,
            'categories': ['Ciencia Ficción', 'Thriller']
        },
        {
            'title': 'El Último Verano',
            'description': 'Drama emotivo sobre la amistad y el paso del tiempo. Cuatro amigos se reencuentran después de 20 años para recordar su último verano juntos.',
            'duration': 115,
            'release_year': 2024,
            'categories': ['Drama', 'Romance']
        },
        {
            'title': 'Guardianes de la Galaxia Perdida',
            'description': 'Épica aventura espacial donde un grupo de héroes debe salvar el universo de una amenaza cósmica. Acción, humor y efectos visuales espectaculares.',
            'duration': 155,
            'release_year': 2023,
            'categories': ['Acción', 'Ciencia Ficción', 'Aventura']
        },
        {
            'title': 'La Casa del Miedo',
            'description': 'Terror psicológico sobre una familia que se muda a una casa antigua con un oscuro secreto. Cada noche, los eventos paranormales se vuelven más intensos.',
            'duration': 108,
            'release_year': 2024,
            'categories': ['Terror', 'Misterio']
        },
        {
            'title': 'Melody',
            'description': 'Musical inspirador sobre una joven cantante que persigue su sueño de convertirse en una estrella mientras enfrenta diversos obstáculos personales.',
            'duration': 122,
            'release_year': 2023,
            'categories': ['Musical', 'Drama']
        },
        {
            'title': 'Detectives Inc.',
            'description': 'Misterio de crimen donde dos detectives con métodos opuestos deben trabajar juntos para resolver una serie de asesinatos en la ciudad.',
            'duration': 135,
            'release_year': 2024,
            'categories': ['Crimen', 'Misterio', 'Thriller']
        }
    ]

    for movie_data in movies_data:
        movie = Movie.query.filter_by(title=movie_data['title']).first()
        if not movie:
            movie = Movie(
                title=movie_data['title'],
                description=movie_data['description'],
                duration=movie_data['duration'],
                release_year=movie_data['release_year'],
                video_path='videos/movies/sample.mp4',  # Necesitarás un video de muestra
                poster_path='images/posters/default.jpg',
                background_path='images/backgrounds/default.jpg'
            )

            # Añadir categorías
            for cat_name in movie_data['categories']:
                category = next((c for c in categories if c.name == cat_name), None)
                if category:
                    movie.categories.append(category)

            db.session.add(movie)
            print(f"✓ Película creada: {movie_data['title']}")

    db.session.commit()


def populate_series(categories):
    """Crear series de ejemplo"""
    series_data = [
        {
            'title': 'Los Secretos de Maple Street',
            'description': 'Drama misterioso sobre los habitantes de una tranquila calle suburbana donde cada familia esconde oscuros secretos.',
            'release_year': 2023,
            'categories': ['Drama', 'Misterio'],
            'seasons': 2,
            'episodes_per_season': 8
        },
        {
            'title': 'Agentes del Caos',
            'description': 'Serie de acción sobre un equipo de espías internacionales que luchan contra organizaciones criminales globales.',
            'release_year': 2024,
            'categories': ['Acción', 'Thriller'],
            'seasons': 1,
            'episodes_per_season': 10
        },
        {
            'title': 'Cocina con Estilo',
            'description': 'Comedia sobre un chef perfeccionista que debe dirigir un restaurante familiar caótico tras heredarlo de su abuela.',
            'release_year': 2023,
            'categories': ['Comedia', 'Familiar'],
            'seasons': 3,
            'episodes_per_season': 12
        },
        {
            'title': 'Viajeros del Tiempo',
            'description': 'Ciencia ficción sobre un grupo de científicos que descubren cómo viajar en el tiempo y deben evitar que la historia sea alterada.',
            'release_year': 2024,
            'categories': ['Ciencia Ficción', 'Aventura'],
            'seasons': 2,
            'episodes_per_season': 10
        },
        {
            'title': 'Reino de Dragones',
            'description': 'Fantasía épica sobre la lucha por el trono de un reino mágico donde dragones y humanos coexisten.',
            'release_year': 2023,
            'categories': ['Fantasía', 'Aventura', 'Drama'],
            'seasons': 4,
            'episodes_per_season': 10
        }
    ]

    for series_info in series_data:
        serie = Series.query.filter_by(title=series_info['title']).first()
        if not serie:
            serie = Series(
                title=series_info['title'],
                description=series_info['description'],
                release_year=series_info['release_year'],
                poster_path='images/posters/default.jpg',
                background_path='images/backgrounds/default.jpg'
            )

            # Añadir categorías
            for cat_name in series_info['categories']:
                category = next((c for c in categories if c.name == cat_name), None)
                if category:
                    serie.categories.append(category)

            db.session.add(serie)
            db.session.flush()  # Para obtener el ID

            # Crear episodios
            for season in range(1, series_info['seasons'] + 1):
                for ep_num in range(1, series_info['episodes_per_season'] + 1):
                    episode = Episode(
                        series_id=serie.id,
                        season_number=season,
                        episode_number=ep_num,
                        title=f"Episodio {ep_num}: {'Piloto' if season == 1 and ep_num == 1 else f'Capítulo {ep_num}'}",
                        description=f"Episodio {ep_num} de la temporada {season} de {serie.title}. Una nueva aventura llena de sorpresas.",
                        duration=45,
                        video_path='videos/series/sample.mp4',  # Necesitarás un video de muestra
                        thumbnail_path='images/posters/default.jpg'
                    )
                    db.session.add(episode)

            print(f"✓ Serie creada: {series_info['title']} ({series_info['seasons']} temporadas)")

    db.session.commit()


def populate_users():
    """Crear usuarios de prueba"""
    users_data = [
        {
            'username': 'usuario_prueba',
            'email': 'usuario@carflix.com',
            'password': 'usuario123',
            'is_admin': False
        },
        {
            'username': 'maria_lopez',
            'email': 'maria@example.com',
            'password': 'maria123',
            'is_admin': False
        },
        {
            'username': 'juan_perez',
            'email': 'juan@example.com',
            'password': 'juan123',
            'is_admin': False
        }
    ]

    for user_data in users_data:
        user = User.query.filter_by(email=user_data['email']).first()
        if not user:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                is_admin=user_data['is_admin']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            print(f"✓ Usuario creado: {user_data['username']} ({user_data['email']})")

    db.session.commit()


def create_sample_files():
    """Crear estructura de archivos de muestra"""
    directories = [
        'app/static/images/profiles',
        'app/static/videos/movies',
        'app/static/videos/series'
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    print("\n✓ Estructura de carpetas creada")
    print("\nNOTA: Recuerda que necesitas:")
    print("  - Un video de muestra en: app/static/videos/movies/sample.mp4")
    print("  - Un video de muestra en: app/static/videos/series/sample.mp4")
    print("  - Una imagen por defecto en: app/static/images/posters/default.jpg")
    print("  - Una imagen por defecto en: app/static/images/backgrounds/default.jpg")


def main():
    """Función principal"""
    app = create_app()

    with app.app_context():
        print("=" * 60)
        print("🎬 CARFLIX - Poblando base de datos")
        print("=" * 60)
        print()

        # Crear estructura de archivos
        create_sample_files()
        print()

        # Poblar categorías
        print("📁 Creando categorías...")
        categories = populate_categories()
        print()

        # Poblar películas
        print("🎬 Creando películas...")
        populate_movies(categories)
        print()

        # Poblar series
        print("📺 Creando series y episodios...")
        populate_series(categories)
        print()

        # Poblar usuarios
        print("👥 Creando usuarios de prueba...")
        populate_users()
        print()

        print("=" * 60)
        print("✅ ¡Base de datos poblada exitosamente!")
        print("=" * 60)
        print()
        print("USUARIOS CREADOS:")
        print("  Admin: admin@carflix.com / admin123")
        print("  Usuario: usuario@carflix.com / usuario123")
        print("  Usuario: maria@example.com / maria123")
        print("  Usuario: juan@example.com / juan123")
        print()
        print("CONTENIDO CREADO:")
        print(f"  - {Category.query.count()} categorías")
        print(f"  - {Movie.query.count()} películas")
        print(f"  - {Series.query.count()} series")
        print(f"  - {Episode.query.count()} episodios")
        print(f"  - {User.query.count()} usuarios")
        print()


if __name__ == '__main__':
    main()