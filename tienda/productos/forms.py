from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre', 'descripcion', 'precio', 'precio_oferta', 'stock', 'categoria', 'activo')
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        datos = super().clean()
        precio = datos.get('precio')
        oferta = datos.get('precio_oferta')
        if precio and oferta and oferta >= precio:
            self.add_error('precio_oferta', 'La oferta debe ser menor al precio normal.')
        return datos