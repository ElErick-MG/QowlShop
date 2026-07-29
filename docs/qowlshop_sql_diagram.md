# 🗄️ Diagrama SQL Completo

## Estructura de Tablas

### 1. users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    is_seller BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email)
);
```

### 2. categories
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_slug (slug)
);
```

### 3. products
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    image_url VARCHAR(300),
    is_active BOOLEAN NOT NULL DEFAULT 1,
    seller_id INTEGER NOT NULL,
    category_id INTEGER,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (seller_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    
    INDEX idx_code (code),
    INDEX idx_name (name),
    INDEX idx_price (price),
    INDEX idx_seller (seller_id),
    INDEX idx_category (category_id),
    
    CHECK (price >= 0),
    CHECK (stock >= 0)
);
```

### 4. orders
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    buyer_id INTEGER NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (buyer_id) REFERENCES users(id),
    
    INDEX idx_order_number (order_number),
    INDEX idx_buyer (buyer_id),
    INDEX idx_created_at (created_at),
    
    CHECK (total_amount >= 0)
);
```

### 5. order_items
```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    product_code VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (seller_id) REFERENCES users(id),
    
    INDEX idx_order (order_id),
    INDEX idx_product (product_id),
    INDEX idx_seller (seller_id),
    
    CHECK (quantity > 0),
    CHECK (price_at_purchase >= 0),
    CHECK (subtotal >= 0)
);
```

### 6. carts
```sql
CREATE TABLE carts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 7. cart_items
```sql
CREATE TABLE cart_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    added_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cart_id) REFERENCES carts(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    
    INDEX idx_cart (cart_id),
    INDEX idx_product (product_id),
    
    UNIQUE (cart_id, product_id),
    CHECK (quantity > 0)
);
```

## Relaciones

### users → products (1:N)
Un usuario (vendedor) puede tener muchos productos.
```
users.id ←→ products.seller_id
```

### users → orders (1:N)
Un usuario (comprador) puede tener muchas órdenes.
```
users.id ←→ orders.buyer_id
```

### users → order_items (1:N)
Un usuario (vendedor) puede tener muchos items vendidos.
```
users.id ←→ order_items.seller_id
```

### users ↔ cart (1:1)
Un usuario tiene un carrito.
```
users.id ←→ carts.user_id
```

### categories → products (1:N)
Una categoría puede tener muchos productos.
```
categories.id ←→ products.category_id
```

### orders → order_items (1:N)
Una orden tiene muchos items.
```
orders.id ←→ order_items.order_id
```

### products → order_items (1:N)
Un producto puede estar en muchos order_items.
```
products.id ←→ order_items.product_id
```

### cart → cart_items (1:N)
Un carrito tiene muchos items.
```
carts.id ←→ cart_items.cart_id
```

### products → cart_items (1:N)
Un producto puede estar en muchos carritos.
```
products.id ←→ cart_items.product_id
```

## Consultas Útiles

### Productos de un vendedor con stock bajo
```sql
SELECT * FROM products 
WHERE seller_id = ? 
  AND stock < 10 
  AND is_active = 1
ORDER BY stock ASC;
```

### Total de ventas de un vendedor
```sql
SELECT SUM(subtotal) as total_ventas
FROM order_items
WHERE seller_id = ?;
```

### Productos más vendidos
```sql
SELECT 
    p.id,
    p.name,
    SUM(oi.quantity) as total_vendido
FROM products p
JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.id, p.name
ORDER BY total_vendido DESC
LIMIT 10;
```

### Compras de un usuario
```sql
SELECT 
    o.order_number,
    o.created_at,
    o.total_amount,
    o.status
FROM orders o
WHERE o.buyer_id = ?
ORDER BY o.created_at DESC;
```

### Historial de ventas detallado
```sql
SELECT 
    oi.product_name,
    oi.quantity,
    oi.price_at_purchase,
    oi.subtotal,
    o.order_number,
    o.created_at,
    u.username as comprador
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
JOIN users u ON o.buyer_id = u.id
WHERE oi.seller_id = ?
ORDER BY oi.created_at DESC;
```

### Productos en carrito con precios actuales
```sql
SELECT 
    p.id,
    p.name,
    p.code,
    p.price,
    p.stock,
    ci.quantity,
    (p.price * ci.quantity) as subtotal
FROM cart_items ci
JOIN products p ON ci.product_id = p.id
WHERE ci.cart_id = ?;
```

## Índices para Optimización

Los siguientes índices mejoran el rendimiento:

```sql
-- Búsqueda de productos
CREATE INDEX idx_product_search ON products(name, code);

-- Filtros de precio
CREATE INDEX idx_product_price_range ON products(price, is_active, stock);

-- Órdenes por comprador y fecha
CREATE INDEX idx_orders_buyer_date ON orders(buyer_id, created_at DESC);

-- Items vendidos por vendedor
CREATE INDEX idx_order_items_seller_date ON order_items(seller_id, created_at DESC);

-- Productos por categoría activos
CREATE INDEX idx_products_category_active ON products(category_id, is_active, stock);
```

## Triggers Sugeridos (Opcional)

### Actualizar updated_at automáticamente
```sql
CREATE TRIGGER update_user_timestamp 
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER update_product_timestamp 
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
    UPDATE products SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

### Validar stock antes de crear OrderItem
```sql
CREATE TRIGGER validate_stock_before_order
BEFORE INSERT ON order_items
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT stock FROM products WHERE id = NEW.product_id) < NEW.quantity
        THEN RAISE(ABORT, 'Stock insuficiente')
    END;
END;
```

## Vistas Útiles

### Vista de productos con información del vendedor
```sql
CREATE VIEW products_with_seller AS
SELECT 
    p.*,
    u.username as seller_username,
    u.email as seller_email,
    c.name as category_name
FROM products p
JOIN users u ON p.seller_id = u.id
LEFT JOIN categories c ON p.category_id = c.id;
```

### Vista de ventas por vendedor
```sql
CREATE VIEW seller_sales_summary AS
SELECT 
    u.id as seller_id,
    u.username,
    COUNT(DISTINCT oi.order_id) as total_orders,
    SUM(oi.quantity) as total_items_sold,
    SUM(oi.subtotal) as total_revenue
FROM users u
JOIN order_items oi ON u.id = oi.seller_id
WHERE u.is_seller = 1
GROUP BY u.id, u.username;
```
