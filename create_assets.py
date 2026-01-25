"""
Script para crear imágenes de prueba para Carflix
Ejecutar: python create_assets.py
"""

import os
from PIL import Image, ImageDraw, ImageFont


def create_default_images():
    """Crear imágenes por defecto"""

    # Crear directorios si no existen
    directories = [
        'app/static/images/profiles',
        'app/static/images/posters',
        'app/static/images/backgrounds'
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # 1. Avatar por defecto (200x200)
    print("Creando avatar por defecto...")
    avatar = Image.new('RGB', (200, 200), color=(16, 185, 129))  # Verde Carflix
    draw = ImageDraw.Draw(avatar)

    # Dibujar círculo para el avatar
    draw.ellipse([20, 20, 180, 180], fill=(255, 255, 255))
    # Cabeza
    draw.ellipse([70, 50, 130, 110], fill=(16, 185, 129))
    # Cuerpo
    draw.ellipse([50, 100, 150, 180], fill=(16, 185, 129))

    avatar.save('app/static/images/default-avatar.png')
    print("✓ Avatar creado: app/static/images/default-avatar.png")

    # 2. Poster por defecto (300x450)
    print("Creando poster por defecto...")
    poster = Image.new('RGB', (300, 450), color=(26, 26, 26))
    draw = ImageDraw.Draw(poster)

    # Gradiente simple
    for i in range(450):
        color = int(26 + (i / 450) * 50)
        draw.line([(0, i), (300, i)], fill=(color, color, color))

    # Texto
    try:
        # Intentar con una fuente del sistema
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        try:
            # En Windows
            font_large = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf", 40)
            font_small = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf", 20)
        except:
            # Fuente por defecto
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

    # Logo CARFLIX
    draw.text((150, 180), "CARFLIX", fill=(16, 185, 129), anchor="mm", font=font_large)
    draw.text((150, 240), "Poster", fill=(179, 179, 179), anchor="mm", font=font_small)

    poster.save('app/static/images/posters/default.jpg', quality=90)
    print("✓ Poster creado: app/static/images/posters/default.jpg")

    # 3. Background por defecto (1920x1080)
    print("Creando background por defecto...")
    background = Image.new('RGB', (1920, 1080), color=(15, 15, 15))
    draw = ImageDraw.Draw(background)

    # Gradiente radial simulado
    center_x, center_y = 960, 540
    for i in range(100):
        offset = i * 15
        color_val = int(15 + i * 0.8)
        draw.ellipse(
            [center_x - offset, center_y - offset, center_x + offset, center_y + offset],
            fill=(color_val, color_val, color_val)
        )

    # Overlay de color
    overlay = Image.new('RGB', (1920, 1080), color=(16, 185, 129))
    background = Image.blend(background, overlay, alpha=0.1)

    draw = ImageDraw.Draw(background)
    try:
        font_huge = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
    except:
        try:
            font_huge = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf", 120)
        except:
            font_huge = ImageFont.load_default()

    draw.text((960, 540), "CARFLIX", fill=(16, 185, 129, 50), anchor="mm", font=font_huge)

    background.save('app/static/images/backgrounds/default.jpg', quality=85)
    print("✓ Background creado: app/static/images/backgrounds/default.jpg")

    print("\n" + "=" * 60)
    print("✅ Todas las imágenes han sido creadas exitosamente!")
    print("=" * 60)


def create_video_instructions():
    """Mostrar instrucciones para videos"""
    print("\n" + "=" * 60)
    print("📹 VIDEOS DE PRUEBA")
    print("=" * 60)
    print("\nNecesitas dos videos MP4 cortos (5-30 segundos):")
    print("  - app/static/videos/movies/sample.mp4")
    print("  - app/static/videos/series/sample.mp4")
    print("\n🔗 OPCIONES PARA DESCARGAR VIDEOS GRATIS:")
    print("\n1. Pexels Videos (https://www.pexels.com/videos/)")
    print("   - Busca cualquier video corto")
    print("   - Descarga en formato MP4")
    print()
    print("2. Pixabay Videos (https://pixabay.com/videos/)")
    print("   - Videos gratuitos sin derechos de autor")
    print("   - Descarga directamente")
    print()
    print("3. Coverr (https://coverr.co/)")
    print("   - Videos de stock gratuitos")
    print("   - Perfecto para pruebas")
    print()
    print("4. CREAR VIDEO SIMPLE CON FFMPEG (si lo tienes instalado):")
    print(
        '   ffmpeg -f lavfi -i color=c=black:s=1280x720:d=10 -vf "drawtext=text=\'VIDEO DE PRUEBA\':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=(h-text_h)/2" -pix_fmt yuv420p app/static/videos/movies/sample.mp4')
    print()
    print("💡 CONSEJO: Puedes usar el MISMO video para ambas carpetas")
    print("   Simplemente copia sample.mp4 a ambas ubicaciones")
    print()


def create_video_directories():
    """Crear directorios para videos"""
    directories = [
        'app/static/videos/movies',
        'app/static/videos/series'
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    print("✓ Directorios de video creados")


def main():
    print("=" * 60)
    print("🎬 CARFLIX - Creando recursos de prueba")
    print("=" * 60)
    print()

    # Verificar si PIL está instalado
    try:
        from PIL import Image
        create_default_images()
        create_video_directories()
        create_video_instructions()
    except ImportError:
        print("❌ Error: Pillow no está instalado")
        print("\nPara instalar Pillow ejecuta:")
        print("  pip install Pillow")
        print("\nDespués vuelve a ejecutar este script:")
        print("  python create_assets.py")
        return

    print("=" * 60)


if __name__ == '__main__':
    main()