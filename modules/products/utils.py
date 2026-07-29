"""
Utilidades para el módulo de productos
"""
import os
from flask import current_app
import uuid
from datetime import datetime

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    ALLOWED_EXTENSIONS = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    """Genera un nombre único para el archivo"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'jpg'
    unique_name = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return unique_name

def save_product_image(image_file):
    """
    Guarda la imagen del producto y retorna la ruta relativa
    
    Args:
        image_file: FileStorage object de Flask
    
    Returns:
        str: Ruta relativa de la imagen guardada o None si falla
    """
    if not image_file or not allowed_file(image_file.filename):
        return None
    
    try:
        # Asegurar que el directorio de uploads existe
        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # Generar nombre único y seguro
        filename = generate_unique_filename(image_file.filename)
        
        # Guardar el archivo
        filepath = os.path.join(upload_folder, filename)
        image_file.save(filepath)
        
        # Retornar ruta relativa para la base de datos
        return f"uploads/products/{filename}"
    
    except Exception as e:
        print(f"Error guardando imagen: {e}")
        return None

def delete_product_image(image_url):
    """
    Elimina una imagen de producto del servidor
    
    Args:
        image_url: Ruta relativa de la imagen
    
    Returns:
        bool: True si se eliminó exitosamente, False si falló
    """
    if not image_url:
        return False
    
    try:
        # Construir ruta completa
        filepath = os.path.join(current_app.root_path, 'static', image_url)
        
        # Eliminar archivo si existe
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        
        return False
    
    except Exception as e:
        print(f"Error eliminando imagen: {e}")
        return False

def get_product_image_url(image_url):
    """Retorna la URL completa de la imagen o una imagen por defecto"""
    if image_url:
        return f"/static/{image_url}"
    return "/static/images/no-image.png"  # Imagen por defecto