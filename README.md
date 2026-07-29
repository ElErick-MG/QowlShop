<div align="center">

# 🛒 QowlShop

### _Plataforma de Comercio Electrónico Multi-Vendedor de Alto Rendimiento_

![Python Version](https://img.shields.io/badge/python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-3.1.1-red?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

<p align="center">
  <b>Un sistema e-commerce completo, modular y escalable construido con Flask y Python.</b><br/>
  Diseñado bajo el patrón de fábrica (Application Factory Pattern) con arquitectura basada en Blueprints, control de acceso basado en roles (RBAC) y gestión automatizada de inventario.
</p>

[📌 Características](#-características-principales) •
[🏗️ Arquitectura](#-arquitectura-del-sistema) •
[⚡ Instalación](#-guía-de-instalación-rápida) •
[🛣️ Rutas](#️-referencia-de-rutas-y-endpoints) •
[🗄️ Base de Datos](#-esquema-de-base-de-datos)

---

</div>

## 📖 Descripción General

**QowlShop** es una solución integral de e-commerce multi-vendedor desarrollada con **Flask 3.0** y **Python**. El sistema permite a los usuarios registrarse como compradores o vendedores, administrar inventarios en tiempo real, procesar órdenes con control automático de stock, gestionar carritos de compra persistentes y administrar la plataforma mediante un panel de control con soporte RBAC.

### 🌟 Puntos Destacados del Proyecto

- **Arquitectura Modular (Blueprints):** Código desacoplado en módulos independientes (`auth`, `products`, `cart`, `orders`, `main`).
- **Control de Acceso por Roles (RBAC):** Permisos diferenciados para Compradores, Vendedores y Administradores.
- **Transacciones e Inventario Atómico:** Descuento y restauración de stock automatizados durante la compra o cancelación de órdenes.
- **Interfaz Moderna y Responsiva:** Maquetación fluida utilizando Bootstrap 5 y Jinja2 templates.
- **Seguridad Integrada:** Hash seguro de contraseñas con Werkzeug, protección contra ataques CSRF con Flask-WTF y sanitización de archivos subidos.

---

## 📌 Características Principales

| Módulo                      | Funcionalidades Destacadas                                                                                                                                                                                                                                                                   |
| :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🔐 **Autenticación & RBAC** | • Registro con opción de perfil de Vendedor.<br/>• Login/Logout seguro gestionado por `Flask-Login`.<br/>• Encriptación PBKDF2/SHA256 para contraseñas.<br/>• Decoradores personalizados `@seller_required` y `@admin_required`.                                                             |
| 📦 **Catálogo & Productos** | • CRUD de productos (Creación, Lectura, Edición, Eliminación).<br/>• Búsqueda por nombre y código SKU único.<br/>• Filtros dinámicos por categorías relacionales y rango de precios.<br/>• Carga y validación de imágenes representativas (`static/uploads/products`).                       |
| 🛒 **Carrito de Compras**   | • Carrito de compras individual y dinámico por usuario.<br/>• Cálculo automático de subtotales y totales globales.<br/>• Validación en tiempo real de disponibilidad de stock antes del Checkout.<br/>• Contador de carrito inyectado globalmente en todas las vistas (`context_processor`). |
| 📋 **Órdenes & Checkout**   | • Generación de número de orden único en cada transacción.<br/>• Deducción automática de stock de los productos comprados.<br/>• Historial detallado de compras para el cliente y de ventas para cada vendedor.<br/>• Cancelación de órdenes pendientes con restitución inmediata de stock.  |
| 🛡️ **Administración**       | • Dashboard con métricas clave del sistema.<br/>• Monitoreo global de usuarios, inventarios y órdenes.                                                                                                                                                                                       |

---

## 🏗️ Arquitectura del Sistema

El proyecto sigue una estructura limpia (**Clean Architecture / Modular Pattern**), dividida en Blueprints para maximizar la mantenibilidad y escalabilidad.

### 📁 Estructura del Proyecto

```text
QowlShop/
├── app.py                          # Factory de la aplicación (create_app)
├── config.py                       # Configuración por entornos (Dev, Test, Prod)
├── extensions.py                   # Inicialización de SQLAlchemy, LoginManager, CSRF
├── run.py                          # Punto de entrada principal
├── requirements.txt                # Dependencias del proyecto
│
├── scripts/                        # Scripts auxiliares y de sembrado
│   └── create_test_products.py     # Script para cargar productos de prueba
│
├── docs/                           # Documentación del proyecto
│   └── qowlshop_sql_diagram.md     # Documentación y consultas SQL optimizadas
│
├── modules/                        # Módulos encapsulados (Blueprints)
│   ├── auth/                       # Modelos, rutas, formularios y decoradores de Auth
│   ├── products/                   # Gestión de productos, categorías y cargas
│   ├── cart/                       # Lógica de carrito de compras y persistencia
│   ├── orders/                     # Procesamiento de órdenes y transacciones
│   └── main/                       # Rutas principales, dashboard y panel admin
│
├── static/                         # Recursos estáticos
│   ├── css/                        # Hojas de estilo personalizadas
│   ├── js/                         # Scripts del cliente
│   └── uploads/products/           # Almacenamiento local de imágenes de productos
│
└── templates/                      # Plantillas base Jinja2
    ├── base.html                   # Layout base de la aplicación
    └── errors/                     # Páginas de error 404, 500
```

---

## 🗄️ Esquema de Base de Datos

QowlShop implementa un modelo relacional robusto para soportar la dinámica multi-vendedor:

```mermaid
erDiagram
    USER ||--o{ PRODUCT : "vende (seller_id)"
    USER ||--o{ ORDER : "compra (buyer_id)"
    USER ||--|| CART : "posee (user_id)"
    CATEGORY ||--o{ PRODUCT : "clasifica"
    ORDER ||--|{ ORDER_ITEM : "contiene"
    PRODUCT ||--o{ ORDER_ITEM : "registra"
    CART ||--|{ CART_ITEM : "contiene"
    PRODUCT ||--o{ CART_ITEM : "incluye"

    USER {
        int id PK
        string username UK
        string email UK
        string password_hash
        string role
        boolean is_seller
    }
    PRODUCT {
        int id PK
        string code UK
        string name
        decimal price
        int stock
        int seller_id FK
        int category_id FK
    }
    ORDER {
        int id PK
        string order_number UK
        int buyer_id FK
        decimal total_amount
        string status
    }
    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        int seller_id FK
        int quantity
        decimal price_at_purchase
        decimal subtotal
    }
    CART {
        int id PK
        int user_id FK UK
    }
    CART_ITEM {
        int id PK
        int cart_id FK
        int product_id FK
        int quantity
    }
```

> 📄 _Para ver las definiciones DDL en SQL, índices de optimización y consultas frecuentes, revisa [qowlshop_sql_diagram.md](file:///d:/levantamientoProyectos/QowlShop/docs/qowlshop_sql_diagram.md)._

---

## ⚡ Guía de Instalación Rápida

Sigue estos pasos para ejecutar **QowlShop** localmente en tu entorno de desarrollo.

### 1. Requisitos Previos

- **Python 3.10+** instalado en tu sistema.
- **Git** para clonar el repositorio.

### 2. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/QowlShop.git
cd QowlShop
```

### 3. Crear y Activar el Entorno Virtual

- **En Windows (PowerShell / CMD):**

  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```

- **En Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno (Opcional)

Crea un archivo `.env` en la raíz del proyecto para personalizar la clave secreta y base de datos:

```env
FLASK_ENV=development
SECRET_KEY=tu-clave-super-secreta-y-segura
DATABASE_URL=sqlite:///qowlshop.db
```

### 6. Poblar la Base de Datos con Datos de Prueba

Al iniciar la aplicación por primera vez se creará la base de datos SQLite y el usuario Administrador. Puedes cargar productos de demostración ejecutando:

```bash
python scripts/create_test_products.py
```

### 7. Ejecutar la Aplicación

```bash
python run.py
```

Accede desde tu navegador web a: **`http://127.0.0.1:5000`**

---

## 👤 Credenciales Iniciales

El sistema genera automáticamente el usuario Administrador por defecto al inicializar la base de datos:

| Rol                          | Correo Electrónico   | Contraseña  | Permisos                                                     |
| :--------------------------- | :------------------- | :---------- | :----------------------------------------------------------- |
| **Administrador / Vendedor** | `admin@qowlshop.com` | `Admin123!` | Acceso completo al sistema, panel admin y venta de productos |

---

## 🛣️ Referencia de Rutas y Endpoints

### 🌐 Rutas Públicas

- `GET /` - Página de inicio con productos destacados y catálogo general.
- `GET /products/` - Lista de productos con buscador y filtro por categoría/precio.
- `GET /products/<id>` - Detalle de un producto específico.
- `GET, POST /auth/login` - Formulario de inicio de sesión.
- `GET, POST /auth/register` - Registro de nuevos usuarios y selección de rol de vendedor.

### 👤 Rutas de Usuarios Autenticados

- `GET /dashboard` - Dashboard del perfil de usuario.
- `GET /cart/` - Vista del carrito de compras.
- `POST /cart/add/<product_id>` - Agregar item al carrito.
- `POST /cart/update/<item_id>` - Modificar cantidad de un item.
- `POST /cart/remove/<item_id>` - Eliminar item del carrito.
- `GET, POST /cart/checkout` - Confirmación y procesamiento de compra.
- `GET /orders/my-purchases` - Historial de compras realizadas por el usuario.
- `GET /auth/logout` - Cerrar sesión activa.

### 🏪 Rutas Exclusivas para Vendedores (`@seller_required`)

- `GET, POST /products/create` - Publicar un nuevo producto.
- `GET, POST /products/<id>/edit` - Modificar información y stock de un producto existente.
- `POST /products/<id>/delete` - Desactivar/eliminar producto.
- `GET /products/my-inventory` - Panel de gestión de inventario del vendedor.
- `GET /orders/my-sales` - Registro de ventas realizadas a clientes.

### 🛡️ Rutas de Administración (`@admin_required`)

- `GET /admin` - Panel general con estadísticas, total de usuarios, ventas globales y productos.

---

## 🧪 Verificación Rápida de Instalación

Puedes ejecutar el siguiente script rápido en tu consola interactiva de Python para validar la salud de tu entorno:

```python
from app import create_app
from modules.auth.models import User
from modules.products.models import Product

app = create_app()
with app.app_context():
    print(f"✅ Total Usuarios: {User.query.count()}")
    print(f"✅ Total Productos: {Product.query.count()}")
    print(f"🛡️ Admin Activo: {User.query.filter_by(role='admin').first().email}")
```

---

## 🗺️ Roadmap de Desarrollos Futuros

- [ ] 💳 Integración con pasarela de pagos en vivo (**Stripe** / **PayPal**).
- [ ] 📧 Envío automático de correos de confirmación de compra y facturación.
- [ ] ⭐ Sistema de reseñas, opiniones y valoraciones con estrellas para productos.
- [ ] 💖 Lista de deseos (_Wishlist_) personalizable.
- [ ] 🎟️ Motor de cupones y códigos de descuento.
- [ ] 📊 Exportación de reportes de ventas a archivos PDF y Excel.

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** [Python 3.10+](https://www.python.org/), [Flask 3.0](https://flask.palletsprojects.com/)
- **ORM & DB:** [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/), [SQLite](https://www.sqlite.org/)
- **Seguridad & Sesiones:** [Flask-Login](https://flask-login.readthedocs.io/), [Flask-WTF](https://flask-wtf.readthedocs.io/), Werkzeug Security
- **Frontend:** [Bootstrap 5](https://getbootstrap.com/), Jinja2 Templates, HTML5/CSS3, JavaScript Vanilla
- **Validación:** WTForms, email-validator

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Puedes usarlo libremente con fines educativos o comerciales.

<div align="center">

**Desarrollado con ❤️ usando Flask & Python - erickdevlml@gmail.com**

</div>
