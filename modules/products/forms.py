"""
Formularios del módulo de productos
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Optional
from modules.products.models import Product

class ProductForm(FlaskForm):
    """Formulario para crear/editar productos"""
    code = StringField('Código del Producto', validators=[
        DataRequired(message='El código es obligatorio'),
        Length(min=3, max=50, message='El código debe tener entre 3 y 50 caracteres')
    ])
    name = StringField('Nombre del Producto', validators=[
        DataRequired(message='El nombre es obligatorio'),
        Length(min=3, max=200, message='El nombre debe tener entre 3 y 200 caracteres')
    ])
    description = TextAreaField('Descripción', validators=[
        Optional(),
        Length(max=2000, message='La descripción no puede exceder 2000 caracteres')
    ])
    price = DecimalField('Precio', validators=[
        DataRequired(message='El precio es obligatorio'),
        NumberRange(min=0.01, message='El precio debe ser mayor a 0')
    ], places=2)
    stock = IntegerField('Stock/Inventario', validators=[
        DataRequired(message='El stock es obligatorio'),
        NumberRange(min=0, message='El stock no puede ser negativo')
    ])
    category_id = SelectField('Categoría', coerce=int, validators=[
        Optional()
    ])
    image = FileField('Imagen del Producto', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Solo se permiten imágenes')
    ])
    submit = SubmitField('Publicar Producto')
    
    def __init__(self, product=None, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.product = product
        
        # Cargar categorías dinámicamente
        from modules.products.models import Category
        self.category_id.choices = [(0, 'Sin categoría')] + [
            (c.id, c.name) for c in Category.query.order_by(Category.name).all()
        ]
    
    def validate_code(self, code):
        """Validar que el código sea único"""
        query = Product.query.filter_by(code=code.data)
        
        # Si estamos editando, excluir el producto actual
        if self.product:
            query = query.filter(Product.id != self.product.id)
        
        if query.first():
            raise ValidationError('Este código ya está en uso. Por favor elige otro.')


class SearchProductForm(FlaskForm):
    """Formulario de búsqueda y filtros de productos"""
    search = StringField('Buscar por nombre o código', validators=[
        Optional(),
        Length(max=100)
    ])
    min_price = DecimalField('Precio mínimo', validators=[
        Optional(),
        NumberRange(min=0, message='El precio no puede ser negativo')
    ], places=2)
    max_price = DecimalField('Precio máximo', validators=[
        Optional(),
        NumberRange(min=0, message='El precio no puede ser negativo')
    ], places=2)
    category_id = SelectField('Categoría', coerce=int, validators=[
        Optional()
    ])
    submit = SubmitField('Buscar')
    
    def __init__(self, *args, **kwargs):
        super(SearchProductForm, self).__init__(*args, **kwargs)
        
        # Cargar categorías dinámicamente
        from modules.products.models import Category
        self.category_id.choices = [(0, 'Todas las categorías')] + [
            (c.id, c.name) for c in Category.query.order_by(Category.name).all()
        ]
    
    def validate(self, **kwargs):
        """Validación personalizada"""
        if not super(SearchProductForm, self).validate(**kwargs):
            return False
        
        # Validar que precio mínimo no sea mayor que precio máximo
        if self.min_price.data and self.max_price.data:
            if self.min_price.data > self.max_price.data:
                self.max_price.errors.append('El precio máximo debe ser mayor al precio mínimo')
                return False
        
        return True


class UpdateStockForm(FlaskForm):
    """Formulario simple para actualizar stock"""
    stock = IntegerField('Nuevo Stock', validators=[
        DataRequired(message='El stock es obligatorio'),
        NumberRange(min=0, message='El stock no puede ser negativo')
    ])
    submit = SubmitField('Actualizar Stock')