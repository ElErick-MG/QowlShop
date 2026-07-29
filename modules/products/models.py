"""
Modelos de Productos y Categorías
"""
from extensions import db
from datetime import datetime
from sqlalchemy import CheckConstraint

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones
    products = db.relationship('Product', back_populates='category', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    __tablename__ = 'products'
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)
    
    # Campos básicos
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    
    # Precio e inventario
    price = db.Column(db.Numeric(10, 2), nullable=False, index=True)
    stock = db.Column(db.Integer, nullable=False, default=0)
    
    # Imagen
    image_url = db.Column(db.String(300))
    
    # Estado
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Foreign Keys
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_positive'),
        CheckConstraint('stock >= 0', name='check_stock_non_negative'),
    )
    
    # Relaciones
    seller = db.relationship('User', back_populates='products', foreign_keys=[seller_id])
    category = db.relationship('Category', back_populates='products')
    order_items = db.relationship('OrderItem', back_populates='product', lazy='dynamic')
    cart_items = db.relationship('CartItem', back_populates='product', lazy='dynamic')
    
    # Métodos útiles
    def is_available(self):
        """Verifica si el producto está disponible para compra"""
        return self.is_active and self.stock > 0
    
    def reduce_stock(self, quantity):
        """Reduce el stock del producto"""
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False
    
    def increase_stock(self, quantity):
        """Aumenta el stock del producto"""
        self.stock += quantity
    
    def __repr__(self):
        return f'<Product {self.code}: {self.name}>'