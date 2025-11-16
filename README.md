# 🛒 QowlShop

Sistema de comercio electrónico con autenticación, gestión de productos, carrito de compras y sistema de órdenes.

## 📁 Estructura del Proyecto

```
qowlshop_app/
│
├── app.py                          # Factory principal de la aplicación
├── config.py                       # Configuraciones centralizadas
├── extensions.py                   # Extensiones compartidas (db, login_manager, csrf)
├── run.py                          # Punto de entrada
├── requirements.txt                # Dependencias
│
├── modules/                        # Módulos de la aplicación
│   ├── auth/                       # Autenticación y usuarios
│   │   ├── __init__.py
│   │   ├── models.py               # User model
│   │   ├── routes.py               # Login, register, logout
│   │   ├── forms.py                # LoginForm, RegisterForm
│   │   ├── decorators.py           # @seller_required, @admin_required
│   │   └── templates/          
│   │       └── auth/
│   │
│   ├── products/                   # Gestión de productos
│   │   ├── __init__.py
│   │   ├── models.py               # Product, Category models
│   │   ├── routes.py               # CRUD productos, búsqueda
│   │   ├── forms.py                # ProductForm, SearchForm
│   │   ├── utils.py                # Manejo de imágenes
│   │   └── templates/
│   │       └── products/
│   │
│   ├── orders/                     # Gestión de órdenes
│   │   ├── __init__.py
│   │   ├── models.py               # Order, OrderItem models
│   │   ├── routes.py               # Historial compras/ventas
│   │   └── templates/
│   │       └── orders/
│   │
│   ├── cart/                       # Carrito de compras
│   │   ├── __init__.py
│   │   ├── models.py               # Cart, CartItem models
│   │   ├── routes.py               # Agregar/quitar productos
│   │   └── templates/
│   │       └── cart/
│   │
│   └── main/                       # Páginas principales
│       ├── __init__.py
│       ├── routes.py               # Index, dashboard, admin
│       └── templates/
│           └── main/
│
├── static/                         # Archivos estáticos
│   ├── css/
│   ├── js/
│   ├── images/
│   └── uploads/                    # Imágenes de productos
│       └── products/
│
└── templates/                      # Templates base
    ├── base.html
    └── errors/
```

## 🗄️ Modelos y Relaciones

### Diagrama ER

```
User (1) ----< (N) Product
  |                    |
  | (comprador)        |
  |                    |
  +----< Order >------+
         (N)     (N)
           \    /
          OrderItem

User (1) --- (1) Cart (1) ----< (N) CartItem >---- (N) Product
```

### Modelos

1. **User**: Usuarios con roles (comprador/vendedor/admin)
2. **Product**: Productos con stock e imágenes
3. **Category**: Categorías de productos
4. **Order**: Órdenes de compra
5. **OrderItem**: Items individuales de cada orden
6. **Cart**: Carrito de compras por usuario
7. **CartItem**: Productos en el carrito

## ✨ Características Implementadas

### 🔐 Autenticación
- ✅ Registro de usuarios (con opción de ser vendedor)
- ✅ Login/Logout con sesiones seguras
- ✅ Contraseñas hasheadas
- ✅ Validaciones de email y contraseña robustas
- ✅ Sistema de roles: comprador(usuario por defecto), vendedor, administrador

### 📦 Productos
- ✅ Publicar productos (solo vendedores)
- ✅ Editar/eliminar productos propios
- ✅ Búsqueda por nombre y código
- ✅ Filtros por precio y categoría
- ✅ Gestión de inventario/stock
- ✅ Carga de imágenes
- ✅ Categorías de productos

### 🛒 Carrito de Compras
- ✅ Agregar productos al carrito
- ✅ Actualizar cantidades
- ✅ Eliminar productos
- ✅ Calcular totales automáticamente
- ✅ Validación de stock disponible

### 📋 Órdenes
- ✅ Crear órdenes desde el carrito
- ✅ Historial de compras
- ✅ Historial de ventas (vendedores)
- ✅ Números de orden únicos
- ✅ Reducción automática de stock
- ✅ Cancelación de órdenes pendientes

### 👥 Roles y Permisos
- ✅ **Usuario normal**: Puede comprar productos
- ✅ **Vendedor**: Puede vender + comprar
- ✅ **Admin**: Acceso completo al sistema

## 🚀 Instalación

### 1. Clonar/Crear el proyecto

```bash
mkdir qowlshop_app
cd qowlshop_app
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear carpetas necesarias

```bash
mkdir -p static/uploads/products
mkdir -p static/images
mkdir -p static/css
mkdir -p static/js
```

### 5. Ejecutar la aplicación

```bash
python run.py
```

La aplicación estará en: `http://127.0.0.1:5000/`

## 👤 Credenciales Iniciales

Se crea automáticamente un usuario administrador:

- **Email:** admin@qowlshop.com
- **Contraseña:** Admin123!
- **Rol:** Administrador + Vendedor

## 📝 Rutas Disponibles

### Públicas
- `/` - Página de inicio con productos destacados
- `/products` - Catálogo de productos (con búsqueda y filtros)
- `/products/<id>` - Detalle de producto
- `/auth/login` - Iniciar sesión
- `/auth/register` - Registrarse

### Usuarios Autenticados
- `/dashboard` - Dashboard personal
- `/cart` - Ver carrito
- `/cart/checkout` - Proceso de checkout
- `/orders/my-purchases` - Historial de compras
- `/auth/logout` - Cerrar sesión

### Solo Vendedores
- `/products/create` - Publicar producto
- `/products/<id>/edit` - Editar producto
- `/products/my-inventory` - Ver inventario
- `/orders/my-sales` - Historial de ventas

### Solo Administradores
- `/admin` - Panel de administración

## 🔧 Configuración

### Variables de Entorno (Opcional)

Crea un archivo `.env`:

```env
SECRET_KEY=tu-clave-secreta-super-segura
FLASK_ENV=development
DATABASE_URL=sqlite:///qowlshop.db
```

### Configuración de Uploads

En `config.py`:
- `UPLOAD_FOLDER`: Carpeta para imágenes
- `MAX_CONTENT_LENGTH`: Tamaño máximo (16MB)
- `ALLOWED_EXTENSIONS`: Formatos permitidos

## 🧪 Probar la Aplicación

### Flujo de prueba completo:

#### 1. Registro de Usuario Vendedor
1. Ve a `/auth/register`
2. Completa el formulario
3. ✅ Marca "Quiero vender productos"
4. Registra con contraseña segura (ej: `Test123!`)

#### 2. Publicar un Producto
1. Login con tu usuario vendedor
2. Ve a `/products/create`
3. Llena los datos:
   - Código: `PROD001`
   - Nombre: `Laptop HP`
   - Precio: `999.99`
   - Stock: `10`
   - Descripción: `Laptop de alta gama`
4. Sube una imagen (opcional)
5. Click en "Publicar Producto"

#### 3. Buscar y Comprar
1. Cierra sesión (o usa modo incógnito)
2. Registra un nuevo usuario (sin marcar vendedor)
3. Ve a `/products`
4. Busca el producto que publicaste
5. Click en el producto
6. Click "Agregar al carrito"
7. Ve a `/cart`
8. Click "Proceder al checkout"
9. Confirma la compra

#### 4. Ver Historial
**Como Comprador:**
- Ve a `/orders/my-purchases`
- Verás tu compra reciente

**Como Vendedor:**
- Login con el usuario vendedor
- Ve a `/orders/my-sales`
- Verás la venta realizada
- Ve a `/products/my-inventory`
- Verás que el stock se redujo automáticamente

#### 5. Panel Admin
1. Login como admin (`admin@qowlshop.com`)
2. Ve a `/admin`
3. Verás estadísticas generales del sistema

---

## 🔍 Verificar Instalación

### Comando de verificación rápida:
```python
# En terminal Python
python

>>> from app import create_app, db
>>> from modules.auth.models import User
>>> from modules.products.models import Product, Category
>>> from modules.orders.models import Order, OrderItem
>>> from modules.cart.models import Cart, CartItem
>>> 
>>> app = create_app()
>>> with app.app_context():
...     print(f"Usuarios: {User.query.count()}")
...     print(f"Categorías: {Category.query.count()}")
...     print(f"Admin existe: {User.query.filter_by(role='admin').first() is not None}")
```

Deberías ver:
```
Usuarios: 1
Categorías: 5
Admin existe: True
```

---

## 🐛 Problemas Comunes

### ❌ ModuleNotFoundError
```
Solución: pip install -r requirements.txt
```

### ❌ No se crea la base de datos
```bash
# Verificar que existe instance/
ls instance/  # o dir instance\ en Windows

# Si no existe, ejecutar:
python
>>> from app import create_app
>>> app = create_app()
>>> with app.app_context():
...     from extensions import db
...     db.create_all()
```

### ❌ Error al subir imágenes
```bash
# Verificar permisos de carpeta
chmod -R 755 static/uploads  # Linux/Mac

# Verificar que la carpeta existe
ls -la static/uploads/products
```

### ❌ CSRF Token Missing
```
Solución: Asegúrate de que csrf está inicializado
y que los formularios tienen {{ form.hidden_tag() }}
```

---

## 📊 Datos de Prueba

Si quieres agregar datos de prueba automáticamente:

```python
# create_test_data.py
from app import create_app, db
from modules.auth.models import User
from modules.products.models import Product, Category

app = create_app()

with app.app_context():
    # Crear vendedor de prueba
    seller = User(
        username='vendedor1',
        email='seller@test.com',
        role='user',
        is_seller=True
    )
    seller.set_password('Test123!')
    db.session.add(seller)
    db.session.commit()
    
    # Crear productos de prueba
    products_data = [
        {'code': 'ELEC001', 'name': 'Laptop Dell', 'price': 1200, 'stock': 5},
        {'code': 'ELEC002', 'name': 'Mouse Logitech', 'price': 25, 'stock': 50},
        {'code': 'BOOK001', 'name': 'Python para todos', 'price': 35, 'stock': 20},
    ]
    
    category = Category.query.filter_by(slug='electronica').first()
    
    for data in products_data:
        product = Product(
            **data,
            seller_id=seller.id,
            category_id=category.id if category else None,
            is_active=True
        )
        db.session.add(product)
    
    db.session.commit()
    print("✅ Datos de prueba creados")
```

Ejecutar: `python create_test_data.py`

---

## 📊 Historias de Usuario Implementadas

✅ **Como vendedor/comprador** quiero registrarme con correo y contraseña  
✅ **Como comprador** necesito buscar/filtrar productos por nombre, código y rango de precio  
✅ **Como vendedor** necesito consultar el inventario actual y ajustar el stock  
✅ **Como vendedor** quiero publicar productos con nombre, precio, descripción e imagen  
✅ **Como comprador** quiero ver los productos que he comprado  
✅ **Como vendedor** quiero ver los productos que he vendido

## 🛠️ Tecnologías Utilizadas

- **Flask 3.0**: Framework web
- **Flask-SQLAlchemy**: ORM
- **Flask-Login**: Gestión de sesiones
- **Flask-WTF**: Formularios y CSRF
- **WTForms**: Validaciones
- **SQLite**: Base de datos
- **Bootstrap 5**: Framework CSS
- **Werkzeug**: Seguridad y uploads

## 💡 Tips

### Acceso rápido al shell de Flask:
```bash
flask shell
# o
python
>>> from app import create_app, db
>>> app = create_app()
>>> app.app_context().push()
>>> # Ahora puedes usar los modelos directamente
```

### Ver todas las rutas:
```bash
python
>>> from app import create_app
>>> app = create_app()
>>> print(app.url_map)
```

### Resetear la base de datos:
```bash
rm instance/qowlshop.db
python run.py  # Se creará de nuevo con datos iniciales
```

## 📚 Cómo Extender la Aplicación

### Agregar un nuevo módulo

1. Crear carpeta en `modules/`
2. Crear `__init__.py`, `models.py`, `routes.py`, `forms.py`
3. Importar y registrar blueprint en `app.py`

Ejemplo:

```python
# En app.py
from modules.mi_modulo import mi_modulo_bp
app.register_blueprint(mi_modulo_bp)
```

### Agregar nuevas relaciones

Edita los modelos correspondientes y agrega las relaciones en ambos lados:

```python
# En Model A
items_b = db.relationship('ModelB', back_populates='model_a')

# En Model B
model_a = db.relationship('ModelA', back_populates='items_b')
```

## 🐛 Solución de Problemas

### La imagen no se sube
- Verifica que la carpeta `static/uploads/products/` existe
- Verifica permisos de escritura
- Revisa el tamaño máximo en `config.py`

### Error al crear órdenes
- Verifica que el producto tenga stock
- Asegúrate de que el carrito no esté vacío

### Imports circulares
- Usa `extensions.py` para extensiones compartidas
- Importa modelos dentro de funciones si es necesario

## 🔒 Seguridad

- ✅ Contraseñas hasheadas con Werkzeug
- ✅ Protección CSRF en todos los formularios
- ✅ Validación de permisos en cada ruta
- ✅ Sanitización de nombres de archivos
- ✅ Validación de tipos de archivo

## ✅ Lista de Verificación Final

Antes de considerar el proyecto completo:

- [ ] ✅ Todos los módulos importan correctamente
- [ ] ✅ La base de datos se crea automáticamente
- [ ] ✅ El usuario admin existe
- [ ] ✅ Las categorías se crean
- [ ] ✅ Puedes registrar usuarios
- [ ] ✅ Puedes crear productos (como vendedor)
- [ ] ✅ Puedes buscar y filtrar productos
- [ ] ✅ Puedes agregar productos al carrito
- [ ] ✅ Puedes completar una compra
- [ ] ✅ El historial de compras funciona
- [ ] ✅ El historial de ventas funciona
- [ ] ✅ El inventario se actualiza correctamente

---

## 🎯 Próximas Funcionalidades Sugeridas

- [ ] Sistema de reviews/calificaciones
- [ ] Wishlist (lista de deseos)
- [ ] Pasarela de pagos (Stripe/PayPal)
- [ ] Notificaciones por email
- [ ] Sistema de mensajería vendedor-comprador
- [ ] Estadísticas avanzadas
- [ ] Export de reportes (PDF/Excel)
- [ ] Múltiples imágenes por producto
- [ ] Sistema de cupones/descuentos
- [ ] Recuperación de contraseña

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y comercial.

---

**Desarrollado con ❤️ usando Flask**
