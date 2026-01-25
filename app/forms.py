from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, \
    SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Optional
from app.models import User


class LoginForm(FlaskForm):
    """Formulario de inicio de sesión"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar Sesión')


class RegistrationForm(FlaskForm):
    """Formulario de registro"""
    username = StringField('Nombre de usuario', validators=[
        DataRequired(),
        Length(min=3, max=64, message='El nombre debe tener entre 3 y 64 caracteres')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[
        DataRequired(),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    password2 = PasswordField('Repetir Contraseña', validators=[
        DataRequired(),
        EqualTo('password', message='Las contraseñas deben coincidir')
    ])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nombre de usuario ya está en uso.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email ya está registrado.')


class MovieForm(FlaskForm):
    """Formulario para películas"""
    title = StringField('Título', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Descripción', validators=[Optional()])
    duration = IntegerField('Duración (minutos)', validators=[Optional()])
    release_year = IntegerField('Año de estreno', validators=[Optional()])
    video = FileField('Archivo de Video', validators=[
        FileAllowed(['mp4', 'avi', 'mkv', 'mov'], 'Solo se permiten archivos de video')
    ])
    poster = FileField('Poster', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Solo se permiten imágenes')
    ])
    background = FileField('Imagen de Fondo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Solo se permiten imágenes')
    ])
    categories = SelectMultipleField('Categorías', coerce=int)
    submit = SubmitField('Guardar Película')


class SeriesForm(FlaskForm):
    """Formulario para series"""
    title = StringField('Título', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Descripción', validators=[Optional()])
    release_year = IntegerField('Año de estreno', validators=[Optional()])
    poster = FileField('Poster', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Solo se permiten imágenes')
    ])
    background = FileField('Imagen de Fondo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Solo se permiten imágenes')
    ])
    categories = SelectMultipleField('Categorías', coerce=int)
    submit = SubmitField('Guardar Serie')


class EpisodeForm(FlaskForm):
    """Formulario para episodios"""
    season_number = IntegerField('Temporada', validators=[DataRequired()])
    episode_number = IntegerField('Número de Episodio', validators=[DataRequired()])
    title = StringField('Título', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Descripción', validators=[Optional()])
    duration = IntegerField('Duración (minutos)', validators=[Optional()])
    video = FileField('Archivo de Video', validators=[
        FileAllowed(['mp4', 'avi', 'mkv', 'mov'], 'Solo se permiten archivos de video')
    ])
    thumbnail = FileField('Miniatura', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Solo se permiten imágenes')
    ])
    submit = SubmitField('Guardar Episodio')


class CategoryForm(FlaskForm):
    """Formulario para categorías"""
    name = StringField('Nombre de la Categoría', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Guardar Categoría')


class SearchForm(FlaskForm):
    """Formulario de búsqueda"""
    query = StringField('Buscar', validators=[DataRequired()])
    submit = SubmitField('Buscar')


class ProfileForm(FlaskForm):
    """Formulario de perfil de usuario"""
    username = StringField('Nombre de usuario', validators=[
        DataRequired(),
        Length(min=3, max=64, message='El nombre debe tener entre 3 y 64 caracteres')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_picture = FileField('Foto de perfil', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Solo se permiten imágenes')
    ])
    submit = SubmitField('Guardar Cambios')


class ChangePasswordForm(FlaskForm):
    """Formulario para cambiar contraseña"""
    current_password = PasswordField('Contraseña actual', validators=[DataRequired()])
    new_password = PasswordField('Nueva contraseña', validators=[
        DataRequired(),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    confirm_password = PasswordField('Confirmar nueva contraseña', validators=[
        DataRequired(),
        EqualTo('new_password', message='Las contraseñas deben coincidir')
    ])
    submit = SubmitField('Cambiar Contraseña')


class AdminUserForm(FlaskForm):
    """Formulario para que el admin cree/edite usuarios"""
    username = StringField('Nombre de usuario', validators=[
        DataRequired(),
        Length(min=3, max=64, message='El nombre debe tener entre 3 y 64 caracteres')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[
        Optional(),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    is_admin = BooleanField('Es administrador')
    submit = SubmitField('Guardar Usuario')