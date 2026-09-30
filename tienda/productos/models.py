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
    precio_oferta = models.PositiveIntegerField(
        'Precio de oferta',
        null=True,
        blank=True,
        help_text='Déjalo vacío si no está en oferta.',
    )
    ICONOS = {'python': '🐍', 'web': '🌐', 'bots': '🤖', 'ui': '🎨'}
    stock = models.PositiveIntegerField(
        'Stock',
        default=10,
        help_text='Unidades disponibles. Si queda en 0 se muestra como «Stock agotado».',
    )

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return self.nombre

    @property
    def en_oferta(self):
        return self.precio_oferta is not None and self.precio_oferta < self.precio

    @property
    def precio_final(self):
        return self.precio_oferta if self.en_oferta else self.precio

    @property
    def descuento(self):
        if not self.en_oferta:
            return 0
        return round((1 - self.precio_oferta / self.precio) * 100)

    @property
    def icono(self):
        return self.ICONOS.get(self.categoria, '📦')

    @property
    def agotado(self):
        return self.stock == 0