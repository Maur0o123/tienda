from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from usuarios.mixins import AdminRequeridoMixin
from .forms import ProductoForm
from .models import Producto

from django.db.models import Q, F
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

def catalogo(request, solo_ofertas=False):
    productos = Producto.objects.filter(activo=True)
    q = request.GET.get('q', '').strip()
    categoria = request.GET.get('categoria', '')

    if q:
        productos = productos.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))

    if categoria in dict(Producto.CATEGORIAS):
        productos = productos.filter(categoria=categoria)
    else:
        categoria = ''

    if solo_ofertas:
        productos = productos.filter(precio_oferta__isnull=False, precio_oferta__lt=F('precio'))

    return render(request, 'productos/catalogo.html', {
        'productos': productos,
        'q': q,
        'categoria': categoria,
        'categorias': Producto.CATEGORIAS,
        'solo_ofertas': solo_ofertas,
    })