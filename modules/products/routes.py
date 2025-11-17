"""
Rutas del módulo de productos
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from extensions import db
from modules.products.models import Product, Category
from modules.products.forms import ProductForm, SearchProductForm, UpdateStockForm
from modules.products.utils import save_product_image, delete_product_image
from modules.auth.decorators import seller_required
from sqlalchemy import or_, and_

products_bp = Blueprint('products', __name__, url_prefix='/products', template_folder='templates')

@products_bp.route('/')
def list_products():
    """Lista todos los productos con búsqueda y filtros"""
    form = SearchProductForm(request.args, meta={'csrf': False})
    
    # Query base: productos activos con stock
    query = Product.query.filter_by(is_active=True).filter(Product.stock > 0)
    
    # Aplicar filtros
    if form.search.data:
        search_term = f"%{form.search.data}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.code.ilike(search_term)
            )
        )
    
    if form.min_price.data:
        query = query.filter(Product.price >= form.min_price.data)
    
    if form.max_price.data:
        query = query.filter(Product.price <= form.max_price.data)
    
    if form.category_id.data and form.category_id.data > 0:
        query = query.filter_by(category_id=form.category_id.data)
    
    # Ordenar por fecha de creación (más recientes primero)
    query = query.order_by(Product.created_at.desc())
    
    # Paginación
    page = request.args.get('page', 1, type=int)
    per_page = 12
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items
    
    return render_template('products/list.html', 
                         products=products, 
                         pagination=pagination,
                         form=form)

@products_bp.route('/<int:id>')
def detail(id):
    """Detalle de un producto"""
    product = Product.query.get_or_404(id)
    return render_template('products/detail.html', product=product)

@products_bp.route('/create', methods=['GET', 'POST'])
@login_required
@seller_required
def create():
    """Crear nuevo producto (solo vendedores)"""
    form = ProductForm()
    
    if form.validate_on_submit():
        # Guardar imagen si se subió
        image_url = None
        if form.image.data:
            image_url = save_product_image(form.image.data)
        
        # Crear producto
        product = Product(
            code=form.code.data,
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            category_id=form.category_id.data if form.category_id.data > 0 else None,
            image_url=image_url,
            seller_id=current_user.id,
            is_active=True
        )
        
        try:
            db.session.add(product)
            db.session.commit()
            flash(f'¡Producto "{product.name}" publicado exitosamente!', 'success')
            return redirect(url_for('products.my_inventory'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear el producto. Por favor intenta de nuevo.', 'danger')
            print(f"Error creando producto: {e}")
    
    return render_template('products/create.html', form=form)

@products_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@seller_required
def edit(id):
    """Editar producto existente"""
    product = Product.query.get_or_404(id)
    
    # Verificar que el producto pertenece al usuario actual
    if product.seller_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    form = ProductForm(product=product, obj=product)
    
    if form.validate_on_submit():
        # Actualizar imagen si se subió una nueva
        if form.image.data:
            # Eliminar imagen anterior
            if product.image_url:
                delete_product_image(product.image_url)
            
            # Guardar nueva imagen
            product.image_url = save_product_image(form.image.data)
        
        # Actualizar campos
        product.code = form.code.data
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.category_id = form.category_id.data if form.category_id.data > 0 else None
        
        try:
            db.session.commit()
            flash(f'Producto "{product.name}" actualizado exitosamente.', 'success')
            return redirect(url_for('products.my_inventory'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el producto.', 'danger')
            print(f"Error actualizando producto: {e}")
    
    return render_template('products/edit.html', form=form, product=product)

@products_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@seller_required
def delete(id):
    """Eliminar producto (soft delete - lo desactiva)"""
    product = Product.query.get_or_404(id)
    
    # Verificar permisos
    if product.seller_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    try:
        # Soft delete: solo desactivar
        product.is_active = False
        db.session.commit()
        flash(f'Producto "{product.name}" eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el producto.', 'danger')
        print(f"Error eliminando producto: {e}")
    
    return redirect(url_for('products.my_inventory'))

@products_bp.route('/<int:id>/reactivate', methods=['POST'])
@login_required
@seller_required
def reactivate(id):
    """Reactivar producto desactivado"""
    product = Product.query.get_or_404(id)
    
    # Verificar permisos
    if product.seller_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    try:
        # Reactivar producto
        product.is_active = True
        db.session.commit()
        flash(f'Producto "{product.name}" reactivado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al reactivar el producto.', 'danger')
        print(f"Error reactivando producto: {e}")
    
    return redirect(url_for('products.my_inventory'))

@products_bp.route('/my-inventory')
@login_required
@seller_required
def my_inventory():
    """Ver inventario del vendedor actual"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    pagination = Product.query.filter_by(seller_id=current_user.id)\
        .order_by(Product.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    products = pagination.items
    
    return render_template('products/my_inventory.html', 
                         products=products, 
                         pagination=pagination)

@products_bp.route('/<int:id>/update-stock', methods=['POST'])
@login_required
@seller_required
def update_stock(id):
    """Actualizar solo el stock de un producto"""
    product = Product.query.get_or_404(id)
    
    # Verificar permisos
    if product.seller_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    form = UpdateStockForm()
    
    if form.validate_on_submit():
        try:
            product.stock = form.stock.data
            db.session.commit()
            flash(f'Stock de "{product.name}" actualizado a {product.stock} unidades.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el stock.', 'danger')
            print(f"Error actualizando stock: {e}")
    
    return redirect(url_for('products.my_inventory'))