"""
Rutas de autenticación
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from modules.auth.models import User
from modules.auth.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Tu cuenta ha sido desactivada. Contacta al administrador.', 'danger')
                return redirect(url_for('auth.login'))
            
            login_user(user, remember=form.remember_me.data)
            flash(f'¡Bienvenido de nuevo, {user.username}!', 'success')
            
            # Redirigir a la página solicitada o al dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Email o contraseña incorrectos. Por favor intenta de nuevo.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Crear nuevo usuario
        user = User(
            username=form.username.data,
            email=form.email.data,
            role='user',
            is_seller=form.is_seller.data  # Si marcó que quiere vender
        )
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            
            # Crear carrito para el nuevo usuario
            from modules.cart.models import Cart
            cart = Cart(user_id=user.id)
            db.session.add(cart)
            db.session.commit()
            
            seller_msg = " Como vendedor, podrás publicar tus productos." if user.is_seller else ""
            flash(f'¡Registro exitoso! Bienvenido, {user.username}.{seller_msg}', 'success')
            
            # Login automático después del registro
            login_user(user)
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Ocurrió un error durante el registro. Por favor intenta de nuevo.', 'danger')
            print(f"Error en registro: {e}")
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('main.index'))