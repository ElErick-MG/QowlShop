"""
Modelos de Carrito de Compras
"""
from extensions import db
from datetime import datetime
from sqlalchemy import CheckConstraint

class Cart(db.Model):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    user = db.relationship('User', back_populates='cart')
    items = db.relationship('CartItem', back_populates='cart', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_total(self):
        """Calcula el total del carrito"""
        return sum(item.get_subtotal() for item in self.items)
    
    def get_item_count(self):
        """Retorna el número total de productos en el carrito"""
        return sum(item.quantity for item in self.items)
    
    def add_item(self, product, quantity=1):
        """Agrega un producto al carrito o actualiza la cantidad si ya existe"""
        cart_item = self.items.filter_by(product_id=product.id).first()
        
        if cart_item:
            # Si ya existe, aumentar la cantidad
            cart_item.quantity += quantity
        else:
            # Si no existe, crear nuevo item
            cart_item = CartItem(
                cart_id=self.id,
                product_id=product.id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        self.updated_at = datetime.utcnow()
        return cart_item
    
    def remove_item(self, product_id):
        """Elimina un producto del carrito"""
        cart_item = self.items.filter_by(product_id=product_id).first()
        if cart_item:
            db.session.delete(cart_item)
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def clear(self):
        """Vacía el carrito"""
        self.items.delete()
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<Cart User:{self.user_id}>'


class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    
    # Cantidad
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # Timestamp
    added_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_cart_quantity_positive'),
        db.UniqueConstraint('cart_id', 'product_id', name='unique_cart_product'),
    )
    
    # Relaciones
    cart = db.relationship('Cart', back_populates='items')
    product = db.relationship('Product', back_populates='cart_items')
    
    def get_subtotal(self):
        """Calcula el subtotal del item"""
        if self.product:
            return float(self.product.price) * self.quantity
        return 0
    
    def update_quantity(self, quantity):
        """Actualiza la cantidad del item"""
        if quantity > 0:
            self.quantity = quantity
            return True
        return False
    
    def __repr__(self):
        return f'<CartItem Product:{self.product_id} x{self.quantity}>'