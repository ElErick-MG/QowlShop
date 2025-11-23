# 🛒 Guía de Implementación: Carrito y Órdenes

**Fecha:** 23 de Noviembre 2025  
**Estado:** Backend completo ✅ | Templates pendientes ❌  

---

## 📋 Resumen Ejecutivo

El backend de **Carrito** y **Órdenes** está **100% funcional**. Solo faltan crear las **plantillas HTML** (templates) para mostrar la información al usuario.

### ✅ Lo que YA está hecho:
- Modelos de base de datos (Cart, CartItem, Order, OrderItem)
- Rutas y lógica de negocio completa
- Validaciones de stock y disponibilidad
- Relaciones entre productos, usuarios y órdenes
- Reducción automática de stock al crear orden
- Cálculo de subtotales y totales

### ❌ Lo que FALTA (tu trabajo):
- Crear 4 templates HTML
- Probar el flujo completo usuario → carrito → orden
- Documentar bugs encontrados (si hay)

---

## 🏗️ Arquitectura del Sistema

```
USUARIO VE PRODUCTO → AGREGA AL CARRITO → HACE CHECKOUT → SE CREA ORDEN → STOCK SE REDUCE
     (products)            (cart)              (cart)        (orders)       (automático)
```

### Flujo Detallado:

1. **Navegación de Productos** ✅ (Ya está)
   - Usuario ve catálogo en `/products`
   - Click en producto → `/products/<id>` (detail.html)
   - Botón "Agregar al carrito"

2. **Carrito de Compras** (TU TRABAJO)
   - `POST /cart/add/<product_id>` → Agrega producto
   - `GET /cart/` → Ver carrito (FALTA template)
   - Actualizar cantidades
   - Eliminar productos
   - Botón "Proceder al checkout"

3. **Creación de Orden** (TU TRABAJO)
   - `POST /orders/create-from-cart` → Crea la orden
   - Valida stock disponible
   - Reduce stock automáticamente
   - Vacía el carrito
   - Genera número de orden único

4. **Historial** (TU TRABAJO)
   - `GET /orders/my-purchases` → Compras del usuario (FALTA template)
   - `GET /orders/my-sales` → Ventas del vendedor (FALTA template)
   - `GET /orders/<id>` → Detalle de orden (FALTA template)

---

## 📁 Estructura de Archivos

### Lo que ya existe:
```
modules/
├── cart/
│   ├── __init__.py          ✅
│   ├── models.py            ✅ (Cart, CartItem)
│   ├── routes.py            ✅ (add, remove, update, clear)
│   └── templates/           ❌ CREAR ESTA CARPETA
│       └── cart/            ❌ CREAR
│           └── view.html    ❌ CREAR ESTE ARCHIVO
│
└── orders/
    ├── __init__.py          ✅
    ├── models.py            ✅ (Order, OrderItem)
    ├── routes.py            ✅ (create, my_purchases, my_sales, detail)
    └── templates/           ❌ CREAR ESTA CARPETA
        └── orders/          ❌ CREAR
            ├── my_purchases.html  ❌ CREAR
            ├── my_sales.html      ❌ CREAR
            └── detail.html        ❌ CREAR
```

---

## 🔧 Rutas Disponibles (Backend)

### 🛒 Carrito (modules/cart/routes.py)

| Ruta | Método | Descripción | Estado |
|------|--------|-------------|--------|
| `/cart/` | GET | Ver carrito | Backend ✅ / Template ❌ |
| `/cart/add/<product_id>` | POST | Agregar producto | ✅ Completo |
| `/cart/update/<item_id>` | POST | Actualizar cantidad | ✅ Completo |
| `/cart/remove/<item_id>` | POST | Eliminar item | ✅ Completo |
| `/cart/clear` | POST | Vaciar carrito | ✅ Completo |

### 📦 Órdenes (modules/orders/routes.py)

| Ruta | Método | Descripción | Estado |
|------|--------|-------------|--------|
| `/orders/my-purchases` | GET | Historial de compras | Backend ✅ / Template ❌ |
| `/orders/my-sales` | GET | Historial de ventas | Backend ✅ / Template ❌ |
| `/orders/<id>` | GET | Detalle de orden | Backend ✅ / Template ❌ |
| `/orders/create-from-cart` | POST | Crear orden | ✅ Completo |
| `/orders/<id>/cancel` | POST | Cancelar orden | ✅ Completo |

---

## 📝 Templates a Crear

### 1. `modules/cart/templates/cart/view.html`

**Propósito:** Mostrar el carrito del usuario con sus productos.

**Datos disponibles en el template:**
```python
cart = {
    'id': int,
    'user': User,
    'items': [CartItem, ...],  # Lista de productos en carrito
    'get_total()': Decimal,     # Total del carrito
    'get_item_count()': int     # Cantidad de items
}

# Cada CartItem tiene:
item = {
    'id': int,
    'product': Product,          # Objeto producto completo
    'quantity': int,
    'get_subtotal()': Decimal    # Precio x cantidad
}
```

**Funcionalidades requeridas:**
- [ ] Mostrar lista de productos en el carrito
- [ ] Para cada producto: imagen, nombre, precio, cantidad, subtotal
- [ ] Botones +/- para ajustar cantidad
- [ ] Botón para eliminar producto
- [ ] Mostrar total general del carrito
- [ ] Botón "Vaciar carrito"
- [ ] Botón "Proceder al checkout" → formulario POST a `/orders/create-from-cart`
- [ ] Mensaje si el carrito está vacío

**Rutas de formularios:**
```html
<!-- Actualizar cantidad -->
<form method="POST" action="{{ url_for('cart.update_item', item_id=item.id) }}">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
    <input type="number" name="quantity" value="{{ item.quantity }}">
    <button type="submit">Actualizar</button>
</form>

<!-- Eliminar item -->
<form method="POST" action="{{ url_for('cart.remove_item', item_id=item.id) }}">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
    <button type="submit">Eliminar</button>
</form>

<!-- Crear orden -->
<form method="POST" action="{{ url_for('orders.create_from_cart') }}">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
    <button type="submit">Confirmar compra</button>
</form>
```

**Referencia de diseño:** Basarse en `products/list.html` y `products/my_inventory.html`

---

### 2. `modules/orders/templates/orders/my_purchases.html`

**Propósito:** Historial de compras del usuario autenticado.

**Datos disponibles:**
```python
orders = [Order, ...]  # Lista de órdenes del usuario
pagination = {
    'page': int,
    'total': int,
    'has_prev': bool,
    'has_next': bool,
    'iter_pages()': [1, 2, 3, ...]
}

# Cada Order tiene:
order = {
    'id': int,
    'order_number': str,          # Ej: "ORD-20251123-0001"
    'buyer': User,
    'items': [OrderItem, ...],
    'status': str,                # 'pending', 'completed', 'cancelled'
    'total': Decimal,
    'created_at': datetime,
    'get_total()': Decimal,
    'get_item_count()': int
}
```

**Funcionalidades requeridas:**
- [ ] Lista de órdenes ordenadas por fecha (más reciente primero)
- [ ] Para cada orden:
  - [ ] Número de orden
  - [ ] Fecha de compra
  - [ ] Estado (badge con color: pending=amarillo, completed=verde, cancelled=rojo)
  - [ ] Total
  - [ ] Cantidad de items
  - [ ] Botón "Ver detalle" → `/orders/<id>`
  - [ ] Botón "Cancelar" si status=='pending' (POST a `/orders/<id>/cancel`)
- [ ] Paginación (10 órdenes por página)
- [ ] Mensaje si no hay compras

**Referencia de diseño:** Similar a `products/my_inventory.html`

---

### 3. `modules/orders/templates/orders/my_sales.html`

**Propósito:** Historial de ventas del vendedor (solo usuarios con `is_seller=True`).

**Datos disponibles:**
```python
order_items = [OrderItem, ...]  # Items vendidos
pagination = {...}
total_sales = Decimal           # Total vendido
total_items_sold = int          # Cantidad de productos vendidos

# Cada OrderItem tiene:
item = {
    'id': int,
    'order': Order,              # Orden a la que pertenece
    'product': Product,
    'quantity': int,
    'price': Decimal,            # Precio al momento de venta
    'subtotal': Decimal,         # price * quantity
    'seller': User,              # Siempre será current_user
    'created_at': datetime
}
```

**Funcionalidades requeridas:**
- [ ] Estadísticas en la parte superior:
  - [ ] Total de ventas (en dinero)
  - [ ] Total de items vendidos (cantidad)
- [ ] Tabla de ventas con columnas:
  - [ ] Fecha
  - [ ] Número de orden (`item.order.order_number`)
  - [ ] Producto vendido
  - [ ] Cantidad
  - [ ] Precio unitario
  - [ ] Subtotal
  - [ ] Comprador (`item.order.buyer.username`)
- [ ] Paginación (20 items por página)
- [ ] Mensaje si no hay ventas

**Referencia de diseño:** Usar tabla similar al README.md o `my_inventory.html`

---

### 4. `modules/orders/templates/orders/detail.html`

**Propósito:** Detalle completo de una orden específica.

**Datos disponibles:**
```python
order = {
    'id': int,
    'order_number': str,
    'buyer': User,
    'items': [OrderItem, ...],
    'status': str,
    'total': Decimal,
    'created_at': datetime,
    'updated_at': datetime
}

# Cada OrderItem en order.items:
item = {
    'product': Product,
    'quantity': int,
    'price': Decimal,
    'subtotal': Decimal,
    'seller': User              # Vendedor del producto
}
```

**Funcionalidades requeridas:**
- [ ] Encabezado con:
  - [ ] Número de orden (grande)
  - [ ] Estado con badge colorido
  - [ ] Fecha de compra
- [ ] Información del comprador:
  - [ ] Nombre
  - [ ] Email
- [ ] Lista de productos comprados:
  - [ ] Imagen del producto
  - [ ] Nombre
  - [ ] Código
  - [ ] Cantidad
  - [ ] Precio unitario
  - [ ] Subtotal
  - [ ] Vendedor de cada item
- [ ] Resumen de totales:
  - [ ] Subtotal
  - [ ] Total
- [ ] Botón "Cancelar orden" si `status == 'pending'`
- [ ] Botón "Volver a mis compras"

**Referencia de diseño:** Similar a `products/detail.html`

---

## 🗄️ Modelos de Base de Datos (Referencia)

### Cart (Carrito)
```python
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    # Relaciones
    user = db.relationship('User', back_populates='cart')
    items = db.relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')
    
    # Métodos útiles
    def get_total(self): ...       # Suma de todos los subtotales
    def get_item_count(self): ...  # Total de items
    def add_item(product, quantity): ...
    def clear(self): ...           # Vacía el carrito
```

### CartItem (Item en carrito)
```python
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    added_at = db.Column(db.DateTime)
    
    # Relaciones
    cart = db.relationship('Cart', back_populates='items')
    product = db.relationship('Product')
    
    # Métodos
    def get_subtotal(self): ...  # product.price * quantity
```

### Order (Orden/Pedido)
```python
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True)  # Ej: "ORD-20251123-0001"
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20))  # 'pending', 'completed', 'cancelled'
    total = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    # Relaciones
    buyer = db.relationship('User', backref='purchases')
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    
    # Métodos
    def generate_order_number(): ...  # Auto-genera "ORD-YYYYMMDD-XXXX"
    def get_total(self): ...
    def get_item_count(self): ...
```

### OrderItem (Item en orden)
```python
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Vendedor
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))      # Precio al momento de compra
    subtotal = db.Column(db.Numeric(10, 2))   # price * quantity
    created_at = db.Column(db.DateTime)
    
    # Relaciones
    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product')
    seller = db.relationship('User', foreign_keys=[seller_id])
```

---

## 🧪 Cómo Probar el Sistema

### Setup Inicial:
```bash
# 1. Asegúrate de que la app esté corriendo
python run.py

# 2. Login como usuario normal (comprador)
Email: user@test.com
Pass: Test123!

# O crea uno nuevo en /auth/register
```

### Flujo de Prueba Completo:

#### Test 1: Agregar productos al carrito
1. Ve a `/products`
2. Click en cualquier producto
3. Ajusta cantidad (ej: 2 unidades)
4. Click "Agregar al carrito"
5. ✅ Debe redirigir a `/cart/` y mostrar el producto

#### Test 2: Modificar carrito
1. En `/cart/`, cambia la cantidad de un producto
2. ✅ Subtotal debe actualizarse
3. Elimina un producto del carrito
4. ✅ El producto desaparece
5. Agrega más productos diferentes
6. ✅ Total del carrito se calcula correctamente

#### Test 3: Crear orden
1. En `/cart/` con varios productos
2. Click "Proceder al checkout" o "Confirmar compra"
3. ✅ Debe crear la orden y redirigir a `/orders/my-purchases`
4. ✅ El carrito debe quedar vacío
5. ✅ El stock de los productos debe reducirse

#### Test 4: Ver historial de compras
1. Ve a `/orders/my-purchases`
2. ✅ Debe aparecer la orden recién creada
3. Click en "Ver detalle"
4. ✅ Debe mostrar todos los productos comprados

#### Test 5: Como vendedor
1. Login como vendedor (admin@qowlshop.com / Admin123!)
2. Ve a `/orders/my-sales`
3. ✅ Debe mostrar las ventas realizadas
4. ✅ Estadísticas deben ser correctas

#### Test 6: Validaciones
1. Intenta agregar más cantidad de la disponible
2. ✅ Debe mostrar error "Solo hay X unidades disponibles"
3. Intenta crear orden con producto sin stock
4. ✅ Debe rechazar y mostrar error

---

## 🎨 Guía de Diseño

### Colores del Sistema:
- **Primary (Azul):** `#2563eb` - Botones principales
- **Success (Verde):** `#10b981` - Stock disponible, orden completada
- **Warning (Amarillo):** `#f59e0b` - Stock bajo, orden pendiente
- **Danger (Rojo):** `#ef4444` - Sin stock, orden cancelada
- **Secondary (Gris):** `#6b7280` - Texto secundario

### Iconos (Bootstrap Icons):
```html
<i class="bi bi-cart3"></i>          <!-- Carrito -->
<i class="bi bi-bag-check"></i>      <!-- Orden completada -->
<i class="bi bi-clock-history"></i>  <!-- Historial -->
<i class="bi bi-receipt"></i>        <!-- Factura/Orden -->
<i class="bi bi-trash"></i>          <!-- Eliminar -->
<i class="bi bi-plus-circle"></i>    <!-- Aumentar cantidad -->
<i class="bi bi-dash-circle"></i>    <!-- Disminuir cantidad -->
```

### Estructura HTML Base:
Todos los templates deben:
1. Extender `base.html`: `{% extends "base.html" %}`
2. Definir título: `{% block title %}Carrito - QowlShop{% endblock %}`
3. Usar Bootstrap 5 (ya está incluido en base.html)
4. Mantener consistencia visual con otros módulos

### Ejemplo de Badge de Estado:
```html
{% if order.status == 'pending' %}
    <span class="badge bg-warning">Pendiente</span>
{% elif order.status == 'completed' %}
    <span class="badge bg-success">Completada</span>
{% elif order.status == 'cancelled' %}
    <span class="badge bg-danger">Cancelada</span>
{% endif %}
```

---

## 🔍 Filtros de Jinja Disponibles

```python
# En templates puedes usar:
{{ product.price|currency }}              # $1,299.00
{{ order.created_at|datetime('%d/%m/%Y') }}  # 23/11/2025
{{ order.created_at|datetime('%d/%m/%Y %H:%M') }}  # 23/11/2025 14:30
```

---

## 🐛 Problemas Conocidos y Soluciones

### ❌ Error: "No module named 'cart'"
**Solución:** Verifica que `modules/cart/__init__.py` existe y contiene:
```python
from modules.cart.routes import cart_bp
```

### ❌ Error: "TemplateNotFound: cart/view.html"
**Solución:** 
1. Crear carpeta: `modules/cart/templates/cart/`
2. Crear archivo: `view.html` dentro de esa carpeta
3. Verificar que en `routes.py` dice: `template_folder='templates'`

### ❌ Error CSRF Token Missing
**Solución:** Todos los formularios POST deben incluir:
```html
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
```

### ❌ Error: "User has no cart"
**Solución:** El carrito se crea automáticamente en `view_cart()`, no hacer nada.

---

## ✅ Checklist de Implementación

### Antes de empezar:
- [ ] Leer esta guía completa
- [ ] Revisar templates existentes en `modules/products/templates/products/`
- [ ] Tener la aplicación corriendo: `python run.py`
- [ ] Tener al menos 3 productos en la base de datos

### Tareas principales:
- [ ] Crear estructura de carpetas:
  - [ ] `modules/cart/templates/cart/`
  - [ ] `modules/orders/templates/orders/`
  
- [ ] Crear `cart/view.html`:
  - [ ] Lista de productos en carrito
  - [ ] Actualizar cantidad (formulario)
  - [ ] Eliminar productos (formulario)
  - [ ] Total del carrito
  - [ ] Botón checkout
  - [ ] Estado vacío

- [ ] Crear `orders/my_purchases.html`:
  - [ ] Lista de órdenes
  - [ ] Badge de estado
  - [ ] Link a detalle
  - [ ] Botón cancelar (si pending)
  - [ ] Paginación

- [ ] Crear `orders/my_sales.html`:
  - [ ] Estadísticas (total vendido, items)
  - [ ] Tabla de ventas
  - [ ] Información del comprador
  - [ ] Paginación

- [ ] Crear `orders/detail.html`:
  - [ ] Número de orden
  - [ ] Información de compra
  - [ ] Lista de productos
  - [ ] Resumen de totales
  - [ ] Botón cancelar (si pending)

### Pruebas:
- [ ] Flujo completo: producto → carrito → orden
- [ ] Validación de stock
- [ ] Actualizar cantidades
- [ ] Eliminar del carrito
- [ ] Cancelar orden
- [ ] Vista de vendedor funciona
- [ ] Paginación funciona

### Documentación:
- [ ] Screenshots del sistema funcionando
- [ ] Lista de bugs encontrados (si hay)
- [ ] Mejoras sugeridas (opcional)

---

## 📞 Contacto y Soporte

Si encuentras problemas o tienes dudas:
1. Revisa primero los archivos de referencia en `modules/products/templates/`
2. Verifica que las rutas en `routes.py` coincidan con las URLs
3. Usa `print()` en routes.py para debug
4. Revisa la terminal donde corre `python run.py` para ver errores

**Archivos de referencia importantes:**
- `templates/base.html` - Template base con navbar
- `modules/products/templates/products/list.html` - Grid de productos
- `modules/products/templates/products/detail.html` - Detalle con breadcrumb
- `modules/products/templates/products/my_inventory.html` - Tarjetas con acciones

---

## 🎯 Objetivo Final

Cuando termines, un usuario debe poder:
1. ✅ Ver productos en el catálogo
2. ✅ Agregar productos al carrito
3. ✅ Modificar el carrito (cantidades, eliminar)
4. ✅ Crear una orden desde el carrito
5. ✅ Ver su historial de compras
6. ✅ Ver detalle de cada orden
7. ✅ Cancelar órdenes pendientes

Y un vendedor debe poder:
1. ✅ Ver todas sus ventas
2. ✅ Ver estadísticas de ventas
3. ✅ Ver quién compró qué producto

---

**¡Buena suerte!** 🚀

Si tienes dudas sobre la estructura de un template específico, puedes basarte en los templates de productos que ya están completos y funcionando.
