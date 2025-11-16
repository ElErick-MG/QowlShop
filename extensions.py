"""
Extensiones compartidas por todos los módulos
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Inicializar extensiones sin app
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

# Configuración del login manager
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'