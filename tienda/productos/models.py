from django.core.validators import MinValueValidator
from django.db import models


class Producto(models.Model):
    CATEGORIAS = [
        ('python', 'Python'),
        ('web', 'Web'),
        ('bots', 'Bots'),
        ('ui', 'Plantillas UI'),
        ('otros', 'Otros'),
    ]

    nombre = models.CharField('Nombre', max_length=120)
    descripcion = models.TextField('Descripción')
    precio = models.PositiveIntegerField('Precio', validators=[MinValueValidator(1)])
    categoria = models.CharField('Categoría', max_length=20, choices=CATEGORIAS, default='otros')
    activo = models.BooleanField(
        'Publicado',
        default=True,
        help_text='Si lo desmarcas, no se mostrará en la tienda.',
    )
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return self.nombre