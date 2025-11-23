"""
Script para crear productos de prueba en la base de datos de QowlShop.
Ejecutar con: python create_test_products.py
"""

from app import create_app
from extensions import db
from modules.products.models import Product
from modules.auth.models import User

app = create_app()

# Productos de ejemplo por categoría
TEST_PRODUCTS = [
    # Electrónica
    {
        "code": "ELEC001",
        "name": "Laptop HP Pavilion 15",
        "description": "Laptop HP Pavilion 15 pulgadas, procesador Intel Core i5 de 11va generación, 8GB RAM, 512GB SSD. Perfecta para trabajo y estudios. Incluye Windows 11 Home y Office 365 de prueba por 30 días.",
        "price": 15999.00,
        "stock": 15,
        "category_id": 1
    },
    {
        "code": "ELEC002",
        "name": "Mouse Inalámbrico Logitech MX Master 3",
        "description": "Mouse ergonómico premium con sensor de alta precisión de 4000 DPI, batería recargable que dura hasta 70 días, compatible con Windows, Mac y Linux. Incluye botones programables y desplazamiento horizontal.",
        "price": 1899.00,
        "stock": 45,
        "category_id": 1
    },
    {
        "code": "ELEC003",
        "name": "Teclado Mecánico RGB Redragon K556",
        "description": "Teclado mecánico gaming con switches rojos, retroiluminación RGB personalizable, construcción de aluminio resistente. 87 teclas formato TKL, perfecto para gaming y programación.",
        "price": 1299.00,
        "stock": 30,
        "category_id": 1
    },
    {
        "code": "ELEC004",
        "name": "Audífonos Bluetooth Sony WH-1000XM4",
        "description": "Audífonos premium con cancelación de ruido líder en la industria, 30 horas de batería, carga rápida (10 min = 5 hrs), audio de alta resolución LDAC. Incluye estuche de transporte.",
        "price": 6499.00,
        "stock": 8,
        "category_id": 1
    },
    
    # Ropa
    {
        "code": "ROPA001",
        "name": "Playera Polo Ralph Lauren Original",
        "description": "Playera polo 100% algodón piqué, corte clásico, disponible en múltiples colores. Bordado del logo icónico. Talla L. Cuidado fácil, lavable a máquina.",
        "price": 899.00,
        "stock": 25,
        "category_id": 2
    },
    {
        "code": "ROPA002",
        "name": "Jeans Levi's 501 Original Fit",
        "description": "El jean icónico de Levi's en su corte original. Denim de alta calidad, cierre de botones, 100% algodón. Talla 32x32. Diseño atemporal que nunca pasa de moda.",
        "price": 1299.00,
        "stock": 18,
        "category_id": 2
    },
    {
        "code": "ROPA003",
        "name": "Sudadera Nike Sportswear Club",
        "description": "Sudadera con capucha, tejido de felpa suave al tacto, 80% algodón 20% poliéster. Logo bordado, bolsillo canguro frontal. Perfecta para uso casual. Talla M.",
        "price": 799.00,
        "stock": 40,
        "category_id": 2
    },
    
    # Hogar
    {
        "code": "HOGAR001",
        "name": "Cafetera Nespresso Vertuo Plus",
        "description": "Cafetera de cápsulas con tecnología Centrifusion, prepara 5 tamaños de café desde espresso hasta alto. Depósito de agua de 1.7L, apagado automático. Incluye 12 cápsulas de bienvenida.",
        "price": 3499.00,
        "stock": 12,
        "category_id": 3
    },
    {
        "code": "HOGAR002",
        "name": "Aspiradora Robot iRobot Roomba 692",
        "description": "Robot aspirador inteligente con conexión WiFi, compatible con Alexa y Google Assistant. Sistema de limpieza en 3 etapas, sensores anti-caída, recarga automática. Ideal para pisos y alfombras.",
        "price": 5999.00,
        "stock": 7,
        "category_id": 3
    },
    {
        "code": "HOGAR003",
        "name": "Juego de Sartenes Antiadherentes T-fal",
        "description": "Set de 3 sartenes (20, 24 y 28 cm) con recubrimiento antiadherente de titanio, indicador de temperatura Thermo-Spot, aptas para todas las fuentes de calor excepto inducción. Libres de PFOA.",
        "price": 1599.00,
        "stock": 22,
        "category_id": 3
    },
    {
        "code": "HOGAR004",
        "name": "Lámpara LED Inteligente Philips Hue",
        "description": "Foco LED inteligente de 16 millones de colores, control por app o voz (Alexa, Google, Siri). Programación de horarios, consumo de solo 10W equivalente a 60W. Duración de 25,000 horas.",
        "price": 899.00,
        "stock": 35,
        "category_id": 3
    },
    
    # Deportes
    {
        "code": "DEP001",
        "name": "Tenis Nike Air Zoom Pegasus 39",
        "description": "Tenis para correr con tecnología Air Zoom para mayor respuesta, malla transpirable Nike Engineered Mesh, suela de caucho resistente. Talla 9 US (27 cm). Para runners de todos los niveles.",
        "price": 2499.00,
        "stock": 20,
        "category_id": 4
    },
    {
        "code": "DEP002",
        "name": "Mancuernas Ajustables Bowflex 24kg",
        "description": "Par de mancuernas ajustables de 2.5kg a 24kg cada una (17 niveles), sistema de selección rápida con dial, equivalente a 17 pares de mancuernas. Ahorra espacio, perfectas para gimnasio en casa.",
        "price": 7999.00,
        "stock": 5,
        "category_id": 4
    },
    {
        "code": "DEP003",
        "name": "Balón de Fútbol Adidas UCL Official",
        "description": "Balón oficial de la UEFA Champions League, tamaño 5, construcción termosellada sin costuras, superficie texturizada para mejor control. Incluye bomba y bolsa de transporte.",
        "price": 1199.00,
        "stock": 28,
        "category_id": 4
    },
    {
        "code": "DEP004",
        "name": "Yoga Mat Premium Lululemon",
        "description": "Tapete para yoga de 5mm de grosor, superficie antideslizante en ambos lados, látex natural, libre de ftalatos y PVC. Dimensiones 180x60cm, incluye correa de transporte. Color morado.",
        "price": 1899.00,
        "stock": 15,
        "category_id": 4
    },
    
    # Libros
    {
        "code": "LIB001",
        "name": "Cien Años de Soledad - Gabriel García Márquez",
        "description": "Obra maestra del realismo mágico, edición conmemorativa con portada dura. La saga de la familia Buendía en Macondo. 496 páginas. Editorial: Random House. Texto en español.",
        "price": 449.00,
        "stock": 50,
        "category_id": 5
    },
    {
        "code": "LIB002",
        "name": "Clean Code - Robert C. Martin",
        "description": "Guía esencial para escribir código limpio y mantenible. Edición en inglés, 464 páginas. Imprescindible para desarrolladores de software que buscan mejorar sus habilidades de programación.",
        "price": 899.00,
        "stock": 32,
        "category_id": 5
    },
    {
        "code": "LIB003",
        "name": "El Principito - Antoine de Saint-Exupéry",
        "description": "Edición ilustrada del clásico de la literatura universal, incluye las acuarelas originales del autor. Traducción de Bonifacio del Carril. 96 páginas. Editorial: Salamandra.",
        "price": 299.00,
        "stock": 60,
        "category_id": 5
    },
    {
        "code": "LIB004",
        "name": "Sapiens: De animales a dioses - Yuval Noah Harari",
        "description": "Historia de la humanidad desde la Edad de Piedra hasta la actualidad. Best seller internacional traducido a más de 50 idiomas. 496 páginas, pasta blanda. Editorial: Debate.",
        "price": 549.00,
        "stock": 38,
        "category_id": 5
    }
]

def create_test_products():
    """Crea productos de prueba en la base de datos."""
    with app.app_context():
        # Buscar al usuario administrador como vendedor
        admin_user = User.query.filter_by(email='admin@qowlshop.com').first()
        
        if not admin_user:
            print("❌ Error: No se encontró el usuario administrador.")
            print("Por favor, ejecuta primero la aplicación para crear el usuario admin.")
            return
        
        if not admin_user.is_seller:
            print("⚠️  El usuario admin no es vendedor. Actualizando...")
            admin_user.is_seller = True
            db.session.commit()
            print("✅ Usuario admin actualizado como vendedor.")
        
        # Contar productos existentes
        existing_products = Product.query.count()
        print(f"\n📦 Productos actuales en la base de datos: {existing_products}")
        
        # Crear productos
        created_count = 0
        skipped_count = 0
        
        print("\n🔄 Creando productos de prueba...\n")
        
        for product_data in TEST_PRODUCTS:
            # Verificar si el código ya existe
            existing = Product.query.filter_by(code=product_data['code']).first()
            
            if existing:
                print(f"⏭️  Saltando {product_data['code']} - {product_data['name']} (ya existe)")
                skipped_count += 1
                continue
            
            # Crear nuevo producto
            product = Product(
                code=product_data['code'],
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                stock=product_data['stock'],
                category_id=product_data['category_id'],
                seller_id=admin_user.id,
                is_active=True
            )
            
            db.session.add(product)
            print(f"✅ Creado: {product_data['code']} - {product_data['name']} (${product_data['price']:.2f})")
            created_count += 1
        
        # Guardar cambios
        db.session.commit()
        
        # Resumen
        print(f"\n{'='*70}")
        print(f"✨ Proceso completado")
        print(f"{'='*70}")
        print(f"✅ Productos creados: {created_count}")
        print(f"⏭️  Productos saltados: {skipped_count}")
        print(f"📦 Total de productos en DB: {Product.query.count()}")
        print(f"\n💡 Puedes ver los productos en: http://localhost:5000/products/")
        print(f"{'='*70}\n")

if __name__ == '__main__':
    create_test_products()
