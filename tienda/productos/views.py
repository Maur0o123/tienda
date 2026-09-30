from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from usuarios.mixins import AdminRequeridoMixin
from .forms import ProductoForm
from .models import Producto

from django.db.models import Case, F, IntegerField, Q, When
from django.shortcuts import render


class ProductoLista(AdminRequeridoMixin, ListView):
    model = Producto
    template_name = 'productos/lista.html'
    context_object_name = 'productos'


class ProductoCrear(AdminRequeridoMixin, SuccessMessageMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/form.html'
    success_url = reverse_lazy('panel_productos')
    success_message = 'Producto creado correctamente.'


class ProductoEditar(AdminRequeridoMixin, SuccessMessageMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/form.html'
    success_url = reverse_lazy('panel_productos')
    success_message = 'Producto actualizado correctamente.'


class ProductoEliminar(AdminRequeridoMixin, DeleteView):
    model = Producto
    template_name = 'productos/confirmar_eliminar.html'
    success_url = reverse_lazy('panel_productos')

    def form_valid(self, form):
        messages.success(self.request, 'Producto eliminado.')
        return super().form_valid(form)

def _entero(valor):
    """Convierte a entero >= 0, o None si no es válido."""
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        return None
    if numero < 0:
        return None
    return min(numero, 2_000_000_000)


def catalogo(request):
    productos = Producto.objects.filter(activo=True).annotate(
        precio_efectivo=Case(
            When(precio_oferta__isnull=False, precio_oferta__lt=F('precio'), then=F('precio_oferta')),
            default=F('precio'),
            output_field=IntegerField(),
        )
    )

    q = request.GET.get('q', '').strip()
    categoria = request.GET.get('categoria', '')
    minimo = _entero(request.GET.get('precio_min'))
    maximo = _entero(request.GET.get('precio_max'))
    solo_ofertas = request.GET.get('ofertas') == '1'

    if minimo is not None and maximo is not None and minimo > maximo:
        minimo, maximo = maximo, minimo

    if q:
        productos = productos.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))

    if categoria in dict(Producto.CATEGORIAS):
        productos = productos.filter(categoria=categoria)
    else:
        categoria = ''

    if minimo is not None:
        productos = productos.filter(precio_efectivo__gte=minimo)
    if maximo is not None:
        productos = productos.filter(precio_efectivo__lte=maximo)

    if solo_ofertas:
        productos = productos.filter(precio_oferta__isnull=False, precio_oferta__lt=F('precio'))

    return render(request, 'productos/catalogo.html', {
        'productos': productos,
        'q': q,
        'categoria': categoria,
        'categorias': Producto.CATEGORIAS,
        'minimo': minimo,
        'maximo': maximo,
        'solo_ofertas': solo_ofertas,
        'hay_filtros': bool(q or categoria or minimo is not None or maximo is not None or solo_ofertas),
    })