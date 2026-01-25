# 🎬 CARFLIX

Plataforma de streaming de contenidos audiovisuales desarrollada con Python y Flask.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![SQLite](https://img.shields.io/badge/SQLite-3-orange)

## 📋 Descripción

Carflix es una aplicación web que simula una plataforma de streaming similar a Netflix, desarrollada como proyecto de aprendizaje. Permite a los usuarios visualizar películas y series, gestionar favoritos, y acceder a estadísticas detalladas.

## ✨ Características

### Para Usuarios
- 📺 Catálogos de películas y series
- ⭐ Sistema de favoritos
- ✅ Marcar contenido como visto
- 📊 Estadísticas personales con gráficas
- 🔍 Buscador avanzado
- 👤 Gestión de perfil

### Para Administradores
- 🎛️ Panel de administración completo
- 👥 Gestión de usuarios
- 🎬 CRUD de películas y series
- 📈 Estadísticas globales
- 🏆 Rankings de usuarios

## 🚀 Instalación

### Requisitos Previos
- Python 3.14 o superior
- pip

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/TU-USUARIO/carflix.git
cd carflix
```

2. **Crear entorno virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Crear recursos iniciales**
```bash
pip install Pillow
python create_assets.py
```

5. **Añadir videos de prueba**
- Descargar videos MP4 cortos
- Colocar en `app/static/videos/movies/sample.mp4`
- Colocar en `app/static/videos/series/sample.mp4`

6. **Ejecutar la aplicación**
```bash
python run.py
```

7. **Acceder a la aplicación**
```
http://127.0.0.1:5000
```

### Datos de prueba (opcional)
```bash
python populate_db.py
```

## 🔑 Credenciales por Defecto

**Administrador:**
- Email: `admin@carflix.com`
- Contraseña: `admin123`

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python, Flask, SQLAlchemy
- **Frontend:** HTML5, CSS3, JavaScript
- **Base de datos:** SQLite
- **Gráficas:** Chart.js
- **Autenticación:** Flask-Login

## 📂 Estructura del Proyecto
```
Carflix/
├── app/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── forms.py
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

## 👨‍💻 Autor

**Carlos**

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría realizar.

---

⭐ Si te gusta este proyecto, dale una estrella en GitHub!