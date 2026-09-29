from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import ProductoForm
from .models import Producto


class AdminRequeridoMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Sin sesión -> login. Con sesión pero sin ser admin -> 403."""

    def test_func(self):
        return self.request.user.is_staff


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