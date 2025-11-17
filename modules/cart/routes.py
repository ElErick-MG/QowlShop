"""
Rutas del módulo de carrito
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from modules.cart.models import Cart, CartItem
from modules.products.models import Product

cart_bp = Blueprint('cart', __name__, url_prefix='/cart', template_folder='templates')

@cart_bp.route('/')
@login_required
def view_cart():
    """Ver el carrito de compras"""
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    if not cart:
        # Crear carrito si no existe
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    
    return render_template('cart/view.html', cart=cart)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Agregar producto al carrito"""
    product = Product.query.get_or_404(product_id)
    
    # Verificar disponibilidad
    if not product.is_available():
        flash(f'El producto "{product.name}" no está disponible.', 'warning')
        return redirect(url_for('products.detail', id=product_id))
    
    quantity = request.form.get('quantity', 1, type=int)
    
    if quantity <= 0:
        flash('La cantidad debe ser mayor a 0.', 'warning')
        return redirect(url_for('products.detail', id=product_id))
    
    if quantity > product.stock:
        flash(f'Solo hay {product.stock} unidades disponibles.', 'warning')
        return redirect(url_for('products.detail', id=product_id))
    
    # Obtener o crear carrito
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.flush()
    
    # Verificar si el producto ya está en el carrito
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    
    try:
        if cart_item:
            # Verificar que no exceda el stock
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                flash(f'Solo puedes agregar {product.stock - cart_item.quantity} unidades más.', 'warning')
                return redirect(url_for('products.detail', id=product_id))
            
            cart_item.quantity = new_quantity
        else:
            # Agregar nuevo item
            cart.add_item(product, quantity)
        
        db.session.commit()
        flash(f'"{product.name}" agregado al carrito.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al agregar el producto al carrito.', 'danger')
        print(f"Error agregando al carrito: {e}")
    
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update_item(item_id):
    """Actualizar cantidad de un item en el carrito"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    # Verificar que el item pertenece al carrito del usuario
    if cart_item.cart.user_id != current_user.id:
        flash('No tienes permiso para modificar este item.', 'danger')
        return redirect(url_for('cart.view_cart'))
    
    quantity = request.form.get('quantity', 1, type=int)
    
    if quantity <= 0:
        flash('La cantidad debe ser mayor a 0.', 'warning')
        return redirect(url_for('cart.view_cart'))
    
    if quantity > cart_item.product.stock:
        flash(f'Solo hay {cart_item.product.stock} unidades disponibles.', 'warning')
        return redirect(url_for('cart.view_cart'))
    
    try:
        cart_item.quantity = quantity
        db.session.commit()
        flash('Cantidad actualizada.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al actualizar la cantidad.', 'danger')
        print(f"Error actualizando carrito: {e}")
    
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_item(item_id):
    """Eliminar un item del carrito"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    # Verificar permisos
    if cart_item.cart.user_id != current_user.id:
        flash('No tienes permiso para eliminar este item.', 'danger')
        return redirect(url_for('cart.view_cart'))
    
    try:
        product_name = cart_item.product.name
        db.session.delete(cart_item)
        db.session.commit()
        flash(f'"{product_name}" eliminado del carrito.', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el producto.', 'danger')
        print(f"Error eliminando del carrito: {e}")
    
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/clear', methods=['POST'])
@login_required
def clear_cart():
    """Vaciar el carrito completamente"""
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    if cart:
        try:
            cart.clear()
            db.session.commit()
            flash('Carrito vaciado.', 'info')
        except Exception as e:
            db.session.rollback()
            flash('Error al vaciar el carrito.', 'danger')
            print(f"Error vaciando carrito: {e}")
    
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/checkout')
@login_required
def checkout():
    """Página de checkout"""
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    if not cart or cart.get_item_count() == 0:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('products.list_products'))
    
    return render_template('cart/checkout.html', cart=cart)