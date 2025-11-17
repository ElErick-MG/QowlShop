"""
Rutas principales y dashboard
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from modules.auth.decorators import admin_required
from modules.auth.models import User
from modules.products.models import Product
from modules.orders.models import Order, OrderItem
from extensions import db

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
def index():
    """Página de inicio"""
    # Mostrar productos destacados (los más recientes)
    featured_products = Product.query\
        .filter_by(is_active=True)\
        .filter(Product.stock > 0)\
        .order_by(Product.created_at.desc())\
        .limit(8)\
        .all()
    
    return render_template('main/index.html', featured_products=featured_products)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard del usuario"""
    # Estadísticas básicas
    stats = {
        'total_purchases': Order.query.filter_by(buyer_id=current_user.id).count(),
        'total_spent': db.session.query(db.func.sum(Order.total_amount))\
            .filter_by(buyer_id=current_user.id)\
            .scalar() or 0
    }
    
    # Si es vendedor, agregar estadísticas de ventas
    if current_user.can_sell():
        stats['total_products'] = Product.query.filter_by(seller_id=current_user.id).count()
        stats['active_products'] = Product.query\
            .filter_by(seller_id=current_user.id, is_active=True)\
            .count()
        stats['total_sales'] = db.session.query(db.func.sum(OrderItem.subtotal))\
            .filter_by(seller_id=current_user.id)\
            .scalar() or 0
        stats['items_sold'] = db.session.query(db.func.sum(OrderItem.quantity))\
            .filter_by(seller_id=current_user.id)\
            .scalar() or 0
    
    # Órdenes recientes
    recent_orders = Order.query\
        .filter_by(buyer_id=current_user.id)\
        .order_by(Order.created_at.desc())\
        .limit(5)\
        .all()
    
    return render_template('main/dashboard.html', 
                         stats=stats, 
                         recent_orders=recent_orders)

@main_bp.route('/admin')
@login_required
@admin_required
def admin_panel():
    """Panel de administración"""
    # Estadísticas generales
    stats = {
        'total_users': User.query.count(),
        'total_sellers': User.query.filter_by(is_seller=True).count(),
        'total_products': Product.query.count(),
        'active_products': Product.query.filter_by(is_active=True).count(),
        'total_orders': Order.query.count(),
        'total_revenue': db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    }
    
    # Usuarios recientes
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    # Productos recientes
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(10).all()
    
    # Órdenes recientes
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    return render_template('main/admin.html',
                         stats=stats,
                         recent_users=recent_users,
                         recent_products=recent_products,
                         recent_orders=recent_orders)