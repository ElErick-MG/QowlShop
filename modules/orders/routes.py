"""
Rutas del módulo de órdenes
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from extensions import db
from modules.orders.models import Order, OrderItem
from modules.products.models import Product
from modules.auth.decorators import seller_required
from sqlalchemy import desc

orders_bp = Blueprint('orders', __name__, url_prefix='/orders', template_folder='templates')

@orders_bp.route('/my-purchases')
@login_required
def my_purchases():
    """Ver historial de compras del usuario"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = Order.query.filter_by(buyer_id=current_user.id)\
        .order_by(desc(Order.created_at))\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    orders = pagination.items
    
    return render_template('orders/my_purchases.html', 
                         orders=orders, 
                         pagination=pagination)

@orders_bp.route('/my-sales')
@login_required
@seller_required
def my_sales():
    """Ver historial de ventas del vendedor"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Obtener todos los items vendidos por el usuario actual
    pagination = OrderItem.query.filter_by(seller_id=current_user.id)\
        .join(Order)\
        .order_by(desc(OrderItem.created_at))\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    order_items = pagination.items
    
    # Calcular estadísticas
    total_sales = db.session.query(db.func.sum(OrderItem.subtotal))\
        .filter_by(seller_id=current_user.id)\
        .scalar() or 0
    
    total_items_sold = db.session.query(db.func.sum(OrderItem.quantity))\
        .filter_by(seller_id=current_user.id)\
        .scalar() or 0
    
    return render_template('orders/my_sales.html', 
                         order_items=order_items, 
                         pagination=pagination,
                         total_sales=total_sales,
                         total_items_sold=total_items_sold)

@orders_bp.route('/<int:id>')
@login_required
def detail(id):
    """Ver detalle de una orden"""
    order = Order.query.get_or_404(id)
    
    # Solo el comprador o admin pueden ver la orden
    if order.buyer_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    return render_template('orders/detail.html', order=order)

@orders_bp.route('/create-from-cart', methods=['POST'])
@login_required
def create_from_cart():
    """Crear una orden desde el carrito del usuario"""
    from modules.cart.models import Cart
    
    # Obtener carrito del usuario
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    if not cart or cart.get_item_count() == 0:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('cart.view_cart'))
    
    try:
        # Crear nueva orden
        order = Order(buyer_id=current_user.id)
        db.session.add(order)
        db.session.flush()  # Para obtener el order.id
        
        # Crear items de orden desde el carrito
        for cart_item in cart.items:
            product = cart_item.product
            
            # Verificar disponibilidad
            if not product.is_available():
                flash(f'El producto "{product.name}" ya no está disponible.', 'danger')
                db.session.rollback()
                return redirect(url_for('cart.view_cart'))
            
            if product.stock < cart_item.quantity:
                flash(f'Stock insuficiente para "{product.name}". Solo quedan {product.stock} unidades.', 'danger')
                db.session.rollback()
                return redirect(url_for('cart.view_cart'))
            
            # Crear OrderItem
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                seller_id=product.seller_id,
                quantity=cart_item.quantity,
                price_at_purchase=product.price,
                product_name=product.name,
                product_code=product.code
            )
            order_item.calculate_subtotal()
            
            # Reducir stock
            product.reduce_stock(cart_item.quantity)
            
            db.session.add(order_item)
        
        # Calcular total de la orden
        order.calculate_total()
        order.status = 'completed'
        
        # Vaciar carrito
        cart.clear()
        
        db.session.commit()
        
        flash(f'¡Compra realizada exitosamente! Número de orden: {order.order_number}', 'success')
        return redirect(url_for('orders.detail', id=order.id))
    
    except Exception as e:
        db.session.rollback()
        flash('Error al procesar la orden. Por favor intenta de nuevo.', 'danger')
        print(f"Error creando orden: {e}")
        return redirect(url_for('cart.view_cart'))

@orders_bp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel(id):
    """Cancelar una orden (solo si está pendiente)"""
    order = Order.query.get_or_404(id)
    
    # Verificar permisos
    if order.buyer_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    if not order.is_pending():
        flash('Solo se pueden cancelar órdenes pendientes.', 'warning')
        return redirect(url_for('orders.detail', id=id))
    
    try:
        # Devolver stock a los productos
        for item in order.items:
            if item.product:
                item.product.increase_stock(item.quantity)
        
        # Cancelar orden
        order.status = 'cancelled'
        db.session.commit()
        
        flash(f'Orden {order.order_number} cancelada exitosamente.', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Error al cancelar la orden.', 'danger')
        print(f"Error cancelando orden: {e}")
    
    return redirect(url_for('orders.my_purchases'))