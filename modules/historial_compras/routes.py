"""
Rutas para ver el historial de compras del usuario
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user

historial_bp = Blueprint('historial', __name__, url_prefix='/historial', template_folder='templates')


@historial_bp.route('/')
@login_required
def index():
	"""Lista todas las órdenes realizadas por el usuario autenticado."""
	# Importar el modelo Order desde el módulo de órdenes (modelo canónico)
	from modules.orders.models import Order

	orders = Order.query.filter_by(buyer_id=current_user.id).order_by(Order.created_at.desc()).all()
	return render_template('historial.html', orders=orders)
