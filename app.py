"""
Aplicación principal - Factory Pattern
"""
import os
from flask import Flask
from extensions import db, login_manager, csrf
from config import config

def create_app(config_name='development'):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Crear directorio de uploads si no existe
    upload_folder = app.config.get('UPLOAD_FOLDER')
    if upload_folder and not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    # Registrar blueprints
    from modules.auth import auth_bp
    from modules.products import products_bp
    from modules.orders import orders_bp
    from modules.cart import cart_bp
    from modules.main import main_bp
    from modules.historial_compras import historial_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(historial_bp)
    
    # Registrar filtros de plantillas personalizados
    register_template_filters(app)
    
    # Contexto de plantillas global
    @app.context_processor
    def inject_cart_count():
        """Inyectar contador de carrito en todas las plantillas"""
        from flask_login import current_user
        cart_count = 0
        if current_user.is_authenticated:
            from modules.cart.models import Cart
            cart = Cart.query.filter_by(user_id=current_user.id).first()
            if cart:
                cart_count = cart.get_item_count()
        return {'cart_count': cart_count}
    
    # Crear tablas y datos iniciales
    with app.app_context():
        db.create_all()
        create_initial_data()
    
    return app

def register_template_filters(app):
    """Registrar filtros personalizados para las plantillas"""
    
    @app.template_filter('currency')
    def currency_filter(value):
        """Formatea un número como moneda"""
        try:
            return f"${float(value):,.2f}"
        except (ValueError, TypeError):
            return "$0.00"
    
    @app.template_filter('datetime')
    def datetime_filter(value, format='%d/%m/%Y %H:%M'):
        """Formatea una fecha"""
        if value is None:
            return ""
        return value.strftime(format)

def create_initial_data():
    """Crear datos iniciales (admin, categorías)"""
    from modules.auth.models import User
    from modules.products.models import Category
    
    # Crear usuario admin si no existe
    admin = User.query.filter_by(email='admin@qowlshop.com').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@qowlshop.com',
            role='admin',
            is_seller=True
        )
        admin.set_password('Admin123!')
        db.session.add(admin)
        print("✓ Usuario admin creado: admin@qowlshop.com / Admin123!")
    
    # Crear categorías por defecto si no existen
    default_categories = [
        {'name': 'Electrónica', 'slug': 'electronica', 'description': 'Dispositivos electrónicos y gadgets'},
        {'name': 'Ropa', 'slug': 'ropa', 'description': 'Ropa y accesorios de moda'},
        {'name': 'Hogar', 'slug': 'hogar', 'description': 'Artículos para el hogar'},
        {'name': 'Deportes', 'slug': 'deportes', 'description': 'Equipamiento deportivo'},
        {'name': 'Libros', 'slug': 'libros', 'description': 'Libros y material de lectura'},
    ]
    
    for cat_data in default_categories:
        cat = Category.query.filter_by(slug=cat_data['slug']).first()
        if not cat:
            cat = Category(**cat_data)
            db.session.add(cat)
            print(f"✓ Categoría creada: {cat_data['name']}")
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creando datos iniciales: {e}")

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    app.run(debug=True)