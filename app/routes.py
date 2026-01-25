import os
from flask import render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from functools import wraps
from app import db
from app.models import User, Movie, Series, Episode, Category
from app.forms import LoginForm, RegistrationForm, MovieForm, SeriesForm, EpisodeForm, CategoryForm, SearchForm, \
    ProfileForm, ChangePasswordForm, AdminUserForm
from datetime import datetime

# Obtener la instancia de la app
from flask import current_app as app


# ==================== DECORADOR ADMIN ====================

def admin_required(f):
    """Decorador para rutas que requieren permisos de administrador"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('No tienes permisos para acceder a esta página', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)

    return decorated_function


# ==================== UTILIDADES ====================

def allowed_file(filename, allowed_extensions):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_file(file, subfolder):
    """Guarda un archivo y retorna la ruta relativa"""
    if file and file.filename:
        filename = secure_filename(file.filename)
        # Añadir timestamp para evitar duplicados
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"

        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)

        return os.path.join(subfolder, filename).replace('\\', '/')
    return None


# ==================== RUTAS PÚBLICAS ====================

@app.route('/')
@app.route('/index')
def index():
    """Página de inicio/landing"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Email o contraseña incorrectos', 'danger')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('home')

        flash(f'¡Bienvenido {user.username}!', 'success')
        return redirect(next_page)

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de nuevos usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))


# ==================== ÁREA DE USUARIO ====================

@app.route('/home')
@login_required
def home():
    """Página principal del usuario"""
    movies = Movie.query.all()
    series = Series.query.all()
    categories = Category.query.all()

    return render_template('home.html', movies=movies, series=series, categories=categories)


@app.route('/movie/<int:movie_id>')
@login_required
def movie_detail(movie_id):
    """Detalle de película"""
    movie = Movie.query.get_or_404(movie_id)
    is_favorite = movie in current_user.favorite_movies
    is_watched = movie in current_user.watched_movies

    return render_template('movie_detail.html', movie=movie, is_favorite=is_favorite, is_watched=is_watched)


@app.route('/series/<int:series_id>')
@login_required
def series_detail(series_id):
    """Detalle de serie"""
    series = Series.query.get_or_404(series_id)
    is_favorite = series in current_user.favorite_series

    # Organizar episodios por temporada
    seasons = {}
    for episode in series.episodes:
        if episode.season_number not in seasons:
            seasons[episode.season_number] = []
        seasons[episode.season_number].append(episode)

    # Ordenar episodios dentro de cada temporada
    for season in seasons:
        seasons[season].sort(key=lambda x: x.episode_number)

    return render_template('series_detail.html', series=series, seasons=seasons, is_favorite=is_favorite)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """Búsqueda de contenido"""
    form = SearchForm()
    results = {'movies': [], 'series': []}
    query = request.args.get('q', '')

    if query:
        # Buscar en películas
        results['movies'] = Movie.query.filter(
            (Movie.title.ilike(f'%{query}%')) |
            (Movie.description.ilike(f'%{query}%'))
        ).all()

        # Buscar en series
        results['series'] = Series.query.filter(
            (Series.title.ilike(f'%{query}%')) |
            (Series.description.ilike(f'%{query}%'))
        ).all()

        # Buscar por categoría
        category = Category.query.filter(Category.name.ilike(f'%{query}%')).first()
        if category:
            results['movies'].extend(category.movies.all())
            results['series'].extend(category.series.all())
            # Eliminar duplicados
            results['movies'] = list(set(results['movies']))
            results['series'] = list(set(results['series']))

    return render_template('search.html', form=form, results=results, query=query)


@app.route('/my-list')
@login_required
def my_list():
    """Lista de favoritos del usuario"""
    return render_template('my_list.html',
                           favorite_movies=current_user.favorite_movies,
                           favorite_series=current_user.favorite_series)


@app.route('/watched')
@login_required
def watched():
    """Contenido visto por el usuario"""
    return render_template('watched.html',
                           watched_movies=current_user.watched_movies,
                           watched_episodes=current_user.watched_episodes)


# ==================== ACCIONES DE USUARIO ====================

@app.route('/toggle-favorite/movie/<int:movie_id>')
@login_required
def toggle_favorite_movie(movie_id):
    """Agregar/quitar película de favoritos"""
    movie = Movie.query.get_or_404(movie_id)

    if movie in current_user.favorite_movies:
        current_user.favorite_movies.remove(movie)
        flash(f'"{movie.title}" eliminada de tu lista', 'info')
    else:
        current_user.favorite_movies.append(movie)
        flash(f'"{movie.title}" añadida a tu lista', 'success')

    db.session.commit()
    return redirect(request.referrer or url_for('home'))


@app.route('/toggle-favorite/series/<int:series_id>')
@login_required
def toggle_favorite_series(series_id):
    """Agregar/quitar serie de favoritos"""
    series = Series.query.get_or_404(series_id)

    if series in current_user.favorite_series:
        current_user.favorite_series.remove(series)
        flash(f'"{series.title}" eliminada de tu lista', 'info')
    else:
        current_user.favorite_series.append(series)
        flash(f'"{series.title}" añadida a tu lista', 'success')

    db.session.commit()
    return redirect(request.referrer or url_for('home'))


@app.route('/toggle-watched/movie/<int:movie_id>')
@login_required
def toggle_watched_movie(movie_id):
    """Marcar película como vista/no vista"""
    movie = Movie.query.get_or_404(movie_id)

    if movie in current_user.watched_movies:
        current_user.watched_movies.remove(movie)
        flash(f'"{movie.title}" marcada como no vista', 'info')
    else:
        current_user.watched_movies.append(movie)
        flash(f'"{movie.title}" marcada como vista', 'success')

    db.session.commit()
    return redirect(request.referrer or url_for('home'))


@app.route('/toggle-watched/episode/<int:episode_id>')
@login_required
def toggle_watched_episode(episode_id):
    """Marcar episodio como visto/no visto"""
    episode = Episode.query.get_or_404(episode_id)

    if episode in current_user.watched_episodes:
        current_user.watched_episodes.remove(episode)
        flash(f'Episodio marcado como no visto', 'info')
    else:
        current_user.watched_episodes.append(episode)
        flash(f'Episodio marcado como visto', 'success')

    db.session.commit()
    return redirect(request.referrer or url_for('series_detail', series_id=episode.series_id))


# ==================== PERFIL DE USUARIO ====================

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Perfil de usuario"""
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        # Verificar si el username ya existe (y no es el actual)
        if form.username.data != current_user.username:
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('Ese nombre de usuario ya está en uso', 'danger')
                return redirect(url_for('profile'))

        # Verificar si el email ya existe (y no es el actual)
        if form.email.data != current_user.email:
            existing_email = User.query.filter_by(email=form.email.data).first()
            if existing_email:
                flash('Ese email ya está registrado', 'danger')
                return redirect(url_for('profile'))

        current_user.username = form.username.data
        current_user.email = form.email.data

        # Guardar foto de perfil
        if form.profile_picture.data:
            profile_pic = save_file(form.profile_picture.data, 'images/profiles')
            if profile_pic:
                current_user.profile_picture = profile_pic

        db.session.commit()
        flash('Perfil actualizado correctamente', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', form=form)


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Cambiar contraseña"""
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('La contraseña actual es incorrecta', 'danger')
            return redirect(url_for('change_password'))

        current_user.set_password(form.new_password.data)
        db.session.commit()

        flash('Contraseña cambiada correctamente', 'success')
        return redirect(url_for('profile'))

    return render_template('change_password.html', form=form)


@app.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    """Eliminar cuenta de usuario"""
    user_id = current_user.id
    username = current_user.username

    # No permitir que el admin se elimine a sí mismo si es el único admin
    if current_user.is_admin:
        admin_count = User.query.filter_by(is_admin=True).count()
        if admin_count <= 1:
            flash('No puedes eliminar la única cuenta de administrador', 'danger')
            return redirect(url_for('profile'))

    logout_user()
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f'Cuenta de {username} eliminada correctamente', 'info')
    return redirect(url_for('index'))


# ==================== ESTADÍSTICAS ====================

@app.route('/stats')
@login_required
def stats():
    """Estadísticas del usuario"""
    from collections import Counter

    # Películas vistas
    movies_watched = current_user.watched_movies
    movies_count = len(movies_watched)

    # Tiempo en películas
    movies_time = sum([movie.duration for movie in movies_watched if movie.duration]) or 0

    # Episodios vistos
    episodes_watched = current_user.watched_episodes
    episodes_count = len(episodes_watched)

    # Tiempo en series
    series_time = sum([ep.duration for ep in episodes_watched if ep.duration]) or 0

    # Tiempo total
    total_time = movies_time + series_time
    total_hours = total_time // 60
    total_minutes = total_time % 60

    # Favoritos
    favorites_count = len(current_user.favorite_movies) + len(current_user.favorite_series)

    # Categorías más vistas
    categories_list = []
    for movie in movies_watched:
        categories_list.extend([cat.name for cat in movie.categories])
    for episode in episodes_watched:
        if episode.series:
            categories_list.extend([cat.name for cat in episode.series.categories])

    category_counts = Counter(categories_list)
    top_categories = category_counts.most_common(5)

    # Series en progreso
    series_progress = []
    series_dict = {}
    for episode in episodes_watched:
        if episode.series_id not in series_dict:
            series_dict[episode.series_id] = {
                'series': episode.series,
                'watched': 0
            }
        series_dict[episode.series_id]['watched'] += 1

    for series_id, data in series_dict.items():
        series = data['series']
        total_episodes = series.episodes.count()
        watched = data['watched']
        percentage = int((watched / total_episodes * 100)) if total_episodes > 0 else 0

        series_progress.append({
            'id': series.id,
            'title': series.title,
            'poster': series.poster_path,
            'watched': watched,
            'total': total_episodes,
            'percentage': percentage
        })

    # Ordenar por progreso
    series_progress.sort(key=lambda x: x['percentage'], reverse=True)

    stats_data = {
        'movies_watched': movies_count,
        'episodes_watched': episodes_count,
        'total_hours': total_hours,
        'total_minutes': total_minutes,
        'favorites': favorites_count,
        'movies_time': movies_time,
        'series_time': series_time,
        'movies_time_hours': movies_time // 60,
        'movies_time_minutes': movies_time % 60,
        'series_time_hours': series_time // 60,
        'series_time_minutes': series_time % 60,
        'top_categories': top_categories,
        'series_progress': series_progress[:5]  # Top 5
    }

    return render_template('stats.html', stats=stats_data)


@app.route('/admin/stats')
@login_required
@admin_required
def admin_stats():
    """Estadísticas globales para el administrador"""
    from collections import Counter

    # Obtener todos los usuarios (excepto admins para las stats)
    users = User.query.filter_by(is_admin=False).all()

    # Estadísticas por usuario
    user_stats = []
    total_movies_watched = 0
    total_episodes_watched = 0
    total_time = 0

    for user in users:
        movies_count = len(user.watched_movies)
        episodes_count = len(user.watched_episodes)

        movies_time = sum([m.duration for m in user.watched_movies if m.duration]) or 0
        series_time = sum([e.duration for e in user.watched_episodes if e.duration]) or 0
        user_total_time = movies_time + series_time

        total_movies_watched += movies_count
        total_episodes_watched += episodes_count
        total_time += user_total_time

        user_stats.append({
            'username': user.username,
            'movies_watched': movies_count,
            'episodes_watched': episodes_count,
            'total_hours': user_total_time // 60,
            'total_minutes': user_total_time % 60,
            'total_time': user_total_time,
            'favorites': len(user.favorite_movies) + len(user.favorite_series)
        })

    # Ordenar por tiempo total
    user_stats.sort(key=lambda x: x['total_time'], reverse=True)

    # Contenido más popular
    # Películas más vistas
    movie_watch_counts = {}
    for user in users:
        for movie in user.watched_movies:
            movie_watch_counts[movie.id] = movie_watch_counts.get(movie.id, 0) + 1

    popular_movies = []
    for movie_id, count in sorted(movie_watch_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        movie = Movie.query.get(movie_id)
        if movie:
            movie.watch_count = count
            popular_movies.append(movie)

    # Series más vistas (por episodios)
    series_watch_counts = {}
    for user in users:
        for episode in user.watched_episodes:
            series_id = episode.series_id
            series_watch_counts[series_id] = series_watch_counts.get(series_id, 0) + 1

    popular_series = []
    for series_id, count in sorted(series_watch_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        series = Series.query.get(series_id)
        if series:
            series.watch_count = count
            popular_series.append(series)

    global_stats = {
        'total_users': len(users),
        'total_hours': total_time // 60,
        'total_movies_watched': total_movies_watched,
        'total_episodes_watched': total_episodes_watched
    }

    return render_template('admin/stats.html',
                           global_stats=global_stats,
                           user_stats=user_stats,
                           popular_movies=popular_movies,
                           popular_series=popular_series)


# ==================== STREAMING DE VIDEO ====================

@app.route('/video/<path:filename>')
@login_required
def serve_video(filename):
    """Servir archivos de video"""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


# ==================== ÁREA DE ADMINISTRADOR ====================

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Panel de administración"""
    try:
        stats = {
            'users': User.query.count(),
            'movies': Movie.query.count(),
            'series': Series.query.count(),
            'episodes': Episode.query.count(),
            'categories': Category.query.count()
        }
        print(f"DEBUG: Stats = {stats}")  # Debug
        return render_template('admin/dashboard.html', stats=stats)
    except Exception as e:
        print(f"ERROR en admin_dashboard: {e}")  # Debug
        flash(f'Error en el panel de administración: {str(e)}', 'danger')
        return redirect(url_for('home'))


# ==================== ADMIN: USUARIOS ====================

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    """Lista de usuarios"""
    users = User.query.all()
    return render_template('admin/users.html', users=users)


@app.route('/admin/user/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_user():
    """Añadir usuario"""
    form = AdminUserForm()

    if form.validate_on_submit():
        # Verificar si el username ya existe
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Ese nombre de usuario ya existe', 'danger')
            return redirect(url_for('admin_add_user'))

        # Verificar si el email ya existe
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Ese email ya está registrado', 'danger')
            return redirect(url_for('admin_add_user'))

        # Crear usuario
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=form.is_admin.data
        )

        if form.password.data:
            user.set_password(form.password.data)
        else:
            user.set_password('password123')  # Contraseña por defecto

        db.session.add(user)
        db.session.commit()

        flash(f'Usuario "{user.username}" creado correctamente', 'success')
        return redirect(url_for('admin_users'))

    return render_template('admin/user_form.html', form=form, title='Añadir Usuario')


@app.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_user(user_id):
    """Editar usuario"""
    user = User.query.get_or_404(user_id)
    form = AdminUserForm(obj=user)

    if form.validate_on_submit():
        # Verificar username (si cambió)
        if form.username.data != user.username:
            existing = User.query.filter_by(username=form.username.data).first()
            if existing:
                flash('Ese nombre de usuario ya existe', 'danger')
                return redirect(url_for('admin_edit_user', user_id=user_id))

        # Verificar email (si cambió)
        if form.email.data != user.email:
            existing = User.query.filter_by(email=form.email.data).first()
            if existing:
                flash('Ese email ya está registrado', 'danger')
                return redirect(url_for('admin_edit_user', user_id=user_id))

        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data

        # Solo cambiar contraseña si se proporciona una nueva
        if form.password.data:
            user.set_password(form.password.data)

        db.session.commit()
        flash(f'Usuario "{user.username}" actualizado correctamente', 'success')
        return redirect(url_for('admin_users'))

    return render_template('admin/user_form.html', form=form, title='Editar Usuario', user=user)


@app.route('/admin/user/delete/<int:user_id>')
@login_required
@admin_required
def admin_delete_user(user_id):
    """Eliminar usuario"""
    if user_id == current_user.id:
        flash('No puedes eliminar tu propio usuario', 'danger')
        return redirect(url_for('admin_users'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'Usuario "{user.username}" eliminado correctamente', 'success')
    return redirect(url_for('admin_users'))


@app.route('/admin/user/toggle-admin/<int:user_id>')
@login_required
@admin_required
def admin_toggle_admin(user_id):
    """Cambiar permisos de administrador"""
    if user_id == current_user.id:
        flash('No puedes modificar tus propios permisos', 'danger')
        return redirect(url_for('admin_users'))

    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()

    status = "administrador" if user.is_admin else "usuario normal"
    flash(f'"{user.username}" ahora es {status}', 'success')
    return redirect(url_for('admin_users'))


# ==================== ADMIN: PELÍCULAS ====================

@app.route('/admin/movies')
@login_required
@admin_required
def admin_movies():
    """Lista de películas"""
    movies = Movie.query.all()
    return render_template('admin/movies.html', movies=movies)


@app.route('/admin/movie/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_movie():
    """Añadir película"""
    form = MovieForm()
    form.categories.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        movie = Movie(
            title=form.title.data,
            description=form.description.data,
            duration=form.duration.data,
            release_year=form.release_year.data,
            video_path='temp'  # Temporal
        )

        # Guardar video
        if form.video.data:
            video_path = save_file(form.video.data, 'videos/movies')
            if video_path:
                movie.video_path = video_path
            else:
                flash('Error al subir el video', 'danger')
                return redirect(url_for('admin_add_movie'))
        else:
            flash('Debes subir un archivo de video', 'danger')
            return redirect(url_for('admin_add_movie'))

        # Guardar poster
        if form.poster.data:
            movie.poster_path = save_file(form.poster.data, 'images/posters')

        # Guardar fondo
        if form.background.data:
            movie.background_path = save_file(form.background.data, 'images/backgrounds')

        # Añadir categorías
        for cat_id in form.categories.data:
            category = Category.query.get(cat_id)
            if category:
                movie.categories.append(category)

        db.session.add(movie)
        db.session.commit()

        flash(f'Película "{movie.title}" añadida correctamente', 'success')
        return redirect(url_for('admin_movies'))

    return render_template('admin/movie_form.html', form=form, title='Añadir Película')


@app.route('/admin/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_movie(movie_id):
    """Editar película"""
    movie = Movie.query.get_or_404(movie_id)
    form = MovieForm(obj=movie)
    form.categories.choices = [(c.id, c.name) for c in Category.query.all()]

    if request.method == 'GET':
        form.categories.data = [c.id for c in movie.categories]

    if form.validate_on_submit():
        movie.title = form.title.data
        movie.description = form.description.data
        movie.duration = form.duration.data
        movie.release_year = form.release_year.data

        # Actualizar video si se sube uno nuevo
        if form.video.data:
            video_path = save_file(form.video.data, 'videos/movies')
            if video_path:
                movie.video_path = video_path

        # Actualizar poster
        if form.poster.data:
            movie.poster_path = save_file(form.poster.data, 'images/posters')

        # Actualizar fondo
        if form.background.data:
            movie.background_path = save_file(form.background.data, 'images/backgrounds')

        # Actualizar categorías
        movie.categories = []
        for cat_id in form.categories.data:
            category = Category.query.get(cat_id)
            if category:
                movie.categories.append(category)

        db.session.commit()
        flash(f'Película "{movie.title}" actualizada correctamente', 'success')
        return redirect(url_for('admin_movies'))

    return render_template('admin/movie_form.html', form=form, title='Editar Película', movie=movie)


@app.route('/admin/movie/delete/<int:movie_id>')
@login_required
@admin_required
def admin_delete_movie(movie_id):
    """Eliminar película"""
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash(f'Película "{movie.title}" eliminada correctamente', 'success')
    return redirect(url_for('admin_movies'))


# ==================== ADMIN: SERIES ====================

@app.route('/admin/series')
@login_required
@admin_required
def admin_series():
    """Lista de series"""
    series = Series.query.all()
    return render_template('admin/series.html', series=series)


@app.route('/admin/series/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_series():
    """Añadir serie"""
    form = SeriesForm()
    form.categories.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        series = Series(
            title=form.title.data,
            description=form.description.data,
            release_year=form.release_year.data
        )

        # Guardar poster
        if form.poster.data:
            series.poster_path = save_file(form.poster.data, 'images/posters')

        # Guardar fondo
        if form.background.data:
            series.background_path = save_file(form.background.data, 'images/backgrounds')

        # Añadir categorías
        for cat_id in form.categories.data:
            category = Category.query.get(cat_id)
            if category:
                series.categories.append(category)

        db.session.add(series)
        db.session.commit()

        flash(f'Serie "{series.title}" añadida correctamente', 'success')
        return redirect(url_for('admin_series'))

    return render_template('admin/series_form.html', form=form, title='Añadir Serie')


@app.route('/admin/series/edit/<int:series_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_series(series_id):
    """Editar serie"""
    series = Series.query.get_or_404(series_id)
    form = SeriesForm(obj=series)
    form.categories.choices = [(c.id, c.name) for c in Category.query.all()]

    if request.method == 'GET':
        form.categories.data = [c.id for c in series.categories]

    if form.validate_on_submit():
        series.title = form.title.data
        series.description = form.description.data
        series.release_year = form.release_year.data

        # Actualizar poster
        if form.poster.data:
            series.poster_path = save_file(form.poster.data, 'images/posters')

        # Actualizar fondo
        if form.background.data:
            series.background_path = save_file(form.background.data, 'images/backgrounds')

        # Actualizar categorías
        series.categories = []
        for cat_id in form.categories.data:
            category = Category.query.get(cat_id)
            if category:
                series.categories.append(category)

        db.session.commit()
        flash(f'Serie "{series.title}" actualizada correctamente', 'success')
        return redirect(url_for('admin_series'))

    return render_template('admin/series_form.html', form=form, title='Editar Serie', series=series)


@app.route('/admin/series/delete/<int:series_id>')
@login_required
@admin_required
def admin_delete_series(series_id):
    """Eliminar serie"""
    series = Series.query.get_or_404(series_id)
    db.session.delete(series)
    db.session.commit()
    flash(f'Serie "{series.title}" eliminada correctamente', 'success')
    return redirect(url_for('admin_series'))


# ==================== ADMIN: EPISODIOS ====================

@app.route('/admin/series/<int:series_id>/episodes')
@login_required
@admin_required
def admin_episodes(series_id):
    """Lista de episodios de una serie"""
    series = Series.query.get_or_404(series_id)
    episodes = Episode.query.filter_by(series_id=series_id).order_by(Episode.season_number,
                                                                     Episode.episode_number).all()
    return render_template('admin/episodes.html', series=series, episodes=episodes)


@app.route('/admin/series/<int:series_id>/episode/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_episode(series_id):
    """Añadir episodio"""
    series = Series.query.get_or_404(series_id)
    form = EpisodeForm()

    if form.validate_on_submit():
        episode = Episode(
            series_id=series_id,
            season_number=form.season_number.data,
            episode_number=form.episode_number.data,
            title=form.title.data,
            description=form.description.data,
            duration=form.duration.data,
            video_path='temp'
        )

        # Guardar video
        if form.video.data:
            video_path = save_file(form.video.data, 'videos/series')
            if video_path:
                episode.video_path = video_path
            else:
                flash('Error al subir el video', 'danger')
                return redirect(url_for('admin_add_episode', series_id=series_id))
        else:
            flash('Debes subir un archivo de video', 'danger')
            return redirect(url_for('admin_add_episode', series_id=series_id))

        # Guardar miniatura
        if form.thumbnail.data:
            episode.thumbnail_path = save_file(form.thumbnail.data, 'images/posters')

        db.session.add(episode)
        db.session.commit()

        flash(f'Episodio añadido correctamente', 'success')
        return redirect(url_for('admin_episodes', series_id=series_id))

    return render_template('admin/episode_form.html', form=form, series=series, title='Añadir Episodio')


@app.route('/admin/episode/delete/<int:episode_id>')
@login_required
@admin_required
def admin_delete_episode(episode_id):
    """Eliminar episodio"""
    episode = Episode.query.get_or_404(episode_id)
    series_id = episode.series_id
    db.session.delete(episode)
    db.session.commit()
    flash('Episodio eliminado correctamente', 'success')
    return redirect(url_for('admin_episodes', series_id=series_id))


# ==================== ADMIN: CATEGORÍAS ====================

@app.route('/admin/categories', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_categories():
    """Gestionar categorías"""
    form = CategoryForm()
    categories = Category.query.all()

    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash(f'Categoría "{category.name}" añadida correctamente', 'success')
        return redirect(url_for('admin_categories'))

    return render_template('admin/categories.html', form=form, categories=categories)


@app.route('/admin/category/delete/<int:category_id>')
@login_required
@admin_required
def admin_delete_category(category_id):
    """Eliminar categoría"""
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash(f'Categoría "{category.name}" eliminada correctamente', 'success')
    return redirect(url_for('admin_categories'))