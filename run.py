from app import create_app, db

app = create_app()

if __name__ == '__main__':
    print("=" * 50)
    print("🎬 CARFLIX - Plataforma de Streaming")
    print("=" * 50)
    print("Servidor iniciado en: http://127.0.0.1:5000")
    print("Usuario admin por defecto:")
    print("  Email: admin@carflix.com")
    print("  Password: admin123")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5000)