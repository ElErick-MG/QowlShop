"""
Modelo de Usuario para autenticación
"""
from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
    
    # Campos básicos
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Roles y permisos
    role = db.Column(db.String(20), nullable=False, default='user')  # user/admin
    is_seller = db.Column(db.Boolean, default=False, nullable=False)  # Puede vender productos
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    # Productos que el usuario vende (si es vendedor)
    products = db.relationship('Product', back_populates='seller', lazy='dynamic', 
                               foreign_keys='Product.seller_id')
    
    # Órdenes como comprador
    purchases = db.relationship('Order', back_populates='buyer', lazy='dynamic',
                               foreign_keys='Order.buyer_id')
    
    # Items vendidos (para historial de ventas)
    sales = db.relationship('OrderItem', back_populates='seller', lazy='dynamic',
                           foreign_keys='OrderItem.seller_id')
    
    # Carrito de compras
    cart = db.relationship('Cart', back_populates='user', uselist=False, cascade='all, delete-orphan')
    
    # Métodos de contraseña
    def set_password(self, password):
        """Hashea y guarda la contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica si la contraseña es correcta"""
        return check_password_hash(self.password_hash, password)
    
    # Métodos de roles
    def is_admin(self):
        """Verifica si el usuario es administrador"""
        return self.role == 'admin'
    
    def can_sell(self):
        """Verifica si el usuario puede vender productos"""
        return self.is_seller or self.is_admin()
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    """Función requerida por Flask-Login para cargar usuarios"""
    return User.query.get(int(user_id))