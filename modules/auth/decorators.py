"""
Decoradores personalizados para control de acceso
"""
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def seller_required(f):
    """
    Decorador que requiere que el usuario sea vendedor.
    Debe usarse después de @login_required
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Por favor inicia sesión para acceder a esta página.', 'info')
            return redirect(url_for('auth.login'))
        
        if not current_user.can_sell():
            flash('No tienes permisos de vendedor. Contacta al administrador.', 'danger')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorador que requiere que el usuario sea administrador.
    Debe usarse después de @login_required
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Por favor inicia sesión para acceder a esta página.', 'info')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin():
            flash('No tienes permisos de administrador.', 'danger')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function

def buyer_required(f):
    """
    Decorador que simplemente requiere autenticación (cualquier usuario puede comprar).
    Es equivalente a @login_required pero más semántico
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Por favor inicia sesión para realizar una compra.', 'info')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function