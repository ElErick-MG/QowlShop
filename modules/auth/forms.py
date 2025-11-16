"""
Formularios de autenticación
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
import re

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='El email es obligatorio'),
        Email(message='Ingresa un email válido')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria')
    ])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegisterForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[
        DataRequired(message='El nombre de usuario es obligatorio'),
        Length(min=3, max=80, message='El nombre de usuario debe tener entre 3 y 80 caracteres'),
        Regexp('^[A-Za-z0-9_]+$', message='El nombre de usuario solo puede contener letras, números y guiones bajos')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='El email es obligatorio'),
        Email(message='Ingresa un email válido')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
        Length(min=8, message='La contraseña debe tener al menos 8 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message='Debes confirmar tu contraseña'),
        EqualTo('password', message='Las contraseñas deben coincidir')
    ])
    is_seller = BooleanField('Quiero vender productos')
    submit = SubmitField('Registrarse')
    
    def validate_username(self, username):
        """Validación personalizada para verificar que el username no exista"""
        from modules.auth.models import User
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nombre de usuario ya está en uso. Por favor elige otro.')
    
    def validate_email(self, email):
        """Validación personalizada para verificar que el email no exista"""
        from modules.auth.models import User
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email ya está registrado. Por favor usa otro o inicia sesión.')
    
    def validate_password(self, password):
        """Validación personalizada para requisitos de contraseña segura"""
        password_value = password.data
        
        # Al menos una letra mayúscula
        if not re.search(r'[A-Z]', password_value):
            raise ValidationError('La contraseña debe contener al menos una letra mayúscula')
        
        # Al menos una letra minúscula
        if not re.search(r'[a-z]', password_value):
            raise ValidationError('La contraseña debe contener al menos una letra minúscula')
        
        # Al menos un número
        if not re.search(r'[0-9]', password_value):
            raise ValidationError('La contraseña debe contener al menos un número')
        
        # Al menos un carácter especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password_value):
            raise ValidationError('La contraseña debe contener al menos un carácter especial (!@#$%^&*...)')