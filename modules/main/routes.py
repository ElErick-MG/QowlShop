"""
Rutas principales y dashboard
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from modules.auth.decorators import admin_required
from modules.auth.models import User
from modules.products.models import Product, Category
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
    
    # Categorías
    categories = Category.query.order_by(Category.name).all()
    
    return render_template('main/admin.html',
                         stats=stats,
                         recent_users=recent_users,
                         recent_products=recent_products,
                         recent_orders=recent_orders,
                         categories=categories)

# ==================== RUTAS DE ADMINISTRACIÓN ====================

@main_bp.route('/admin/product/<int:id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_product_status(id):
    """Activar/Desactivar un producto"""
    product = Product.query.get_or_404(id)
    
    try:
        product.is_active = not product.is_active
        db.session.commit()
        
        status = "activado" if product.is_active else "desactivado"
        flash(f'Producto "{product.name}" {status} exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al cambiar el estado del producto.', 'danger')
        print(f"Error: {e}")
    
    return redirect(url_for('main.admin_panel'))

@main_bp.route('/admin/product/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_product(id):
    """Eliminar un producto (solo admin)"""
    product = Product.query.get_or_404(id)
    
    try:
        # Verificar si el producto tiene órdenes asociadas
        order_items_count = OrderItem.query.filter_by(product_id=id).count()
        
        if order_items_count > 0:
            # No eliminar, solo desactivar
            product.is_active = False
            db.session.commit()
            flash(f'El producto "{product.name}" ha sido desactivado porque tiene órdenes asociadas.', 'warning')
        else:
            # Eliminar completamente
            product_name = product.name
            db.session.delete(product)
            db.session.commit()
            flash(f'Producto "{product_name}" eliminado permanentemente.', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el producto.', 'danger')
        print(f"Error: {e}")
    
    return redirect(url_for('main.admin_panel'))

@main_bp.route('/admin/user/<int:id>/toggle-seller', methods=['POST'])
@login_required
@admin_required
def toggle_seller_status(id):
    """Convertir usuario en vendedor o viceversa"""
    user = User.query.get_or_404(id)
    
    # No permitir modificar admins
    if user.is_admin():
        flash('No se puede modificar el rol de un administrador.', 'danger')
        return redirect(url_for('main.admin_panel'))
    
    try:
        user.is_seller = not user.is_seller
        db.session.commit()
        
        status = "vendedor" if user.is_seller else "comprador"
        flash(f'Usuario "{user.username}" ahora es {status}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al cambiar el rol del usuario.', 'danger')
        print(f"Error: {e}")
    
    return redirect(url_for('main.admin_panel'))

@main_bp.route('/admin/category/add', methods=['POST'])
@login_required
@admin_required
def add_category():
    """Agregar nueva categoría"""
    name = request.form.get('name', '').strip()
    slug = request.form.get('slug', '').strip()
    description = request.form.get('description', '').strip()
    
    if not name or not slug:
        flash('El nombre y slug son obligatorios.', 'danger')
        return redirect(url_for('main.admin_panel'))
    
    # Verificar que el slug sea único
    existing = Category.query.filter_by(slug=slug).first()
    if existing:
        flash(f'Ya existe una categoría con el slug "{slug}".', 'danger')
        return redirect(url_for('main.admin_panel'))
    
    try:
        category = Category(
            name=name,
            slug=slug,
            description=description
        )
        db.session.add(category)
        db.session.commit()
        
        flash(f'Categoría "{name}" creada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al crear la categoría.', 'danger')
        print(f"Error: {e}")
    
    return redirect(url_for('main.admin_panel'))

@main_bp.route('/admin/category/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(id):
    """Eliminar una categoría"""
    category = Category.query.get_or_404(id)
    
    # Verificar si tiene productos asociados
    products_count = category.products.count()
    
    if products_count > 0:
        return jsonify({
            'success': False,
            'message': f'No se puede eliminar. Tiene {products_count} productos asociados.'
        }), 400
    
    try:
        category_name = category.name
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Categoría "{category_name}" eliminada.'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Error al eliminar la categoría.'
        }), 500
