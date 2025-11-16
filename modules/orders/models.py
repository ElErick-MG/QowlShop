"""
Modelos de Órdenes y OrderItems
"""
from extensions import db
from datetime import datetime
from sqlalchemy import CheckConstraint
import uuid

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Número único de orden
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Comprador
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Total de la orden
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    
    # Estado de la orden
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, completed, cancelled
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('total_amount >= 0', name='check_total_positive'),
    )
    
    # Relaciones
    buyer = db.relationship('User', back_populates='purchases', foreign_keys=[buyer_id])
    items = db.relationship('OrderItem', back_populates='order', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        if not self.order_number:
            self.order_number = self.generate_order_number()
    
    @staticmethod
    def generate_order_number():
        """Genera un número único de orden"""
        return f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
    
    def calculate_total(self):
        """Calcula el total de la orden sumando todos los items"""
        self.total_amount = sum(item.subtotal for item in self.items)
        return self.total_amount
    
    def is_pending(self):
        return self.status == 'pending'
    
    def is_completed(self):
        return self.status == 'completed'
    
    def is_cancelled(self):
        return self.status == 'cancelled'
    
    def __repr__(self):
        return f'<Order {self.order_number}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Detalles del item
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Numeric(10, 2), nullable=False)  # Precio al momento de la compra
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)  # quantity * price_at_purchase
    
    # Información adicional guardada al momento de la compra
    product_name = db.Column(db.String(200), nullable=False)  # Por si el producto se elimina
    product_code = db.Column(db.String(50), nullable=False)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
        CheckConstraint('price_at_purchase >= 0', name='check_price_positive'),
        CheckConstraint('subtotal >= 0', name='check_subtotal_positive'),
    )
    
    # Relaciones
    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product', back_populates='order_items')
    seller = db.relationship('User', back_populates='sales', foreign_keys=[seller_id])
    
    def __init__(self, **kwargs):
        super(OrderItem, self).__init__(**kwargs)
        # Calcular subtotal automáticamente si no se proporciona
        if not self.subtotal and self.quantity and self.price_at_purchase:
            self.subtotal = self.quantity * self.price_at_purchase
    
    def calculate_subtotal(self):
        """Calcula el subtotal del item"""
        self.subtotal = self.quantity * self.price_at_purchase
        return self.subtotal
    
    def __repr__(self):
        return f'<OrderItem {self.product_code} x{self.quantity}>'