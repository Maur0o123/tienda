from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import RegistroForm, PerfilForm
from productos.models import Producto
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView

from .forms import RegistroForm, PerfilForm, UsuarioAdminForm
from .mixins import AdminRequeridoMixin

from django.views import View
from .forms import RegistroForm, PerfilForm, UsuarioAdminForm, ContactoForm
from .models import MensajeContacto


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()

    return render(request, 'registration/register.html', {'form': form})


def home(request):
    destacados = Producto.objects.filter(activo=True)[:3]
    return render(request, 'home.html', {'destacados': destacados})

@login_required
def perfil(request):
    usuario = User.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=usuario)
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, 'Perfil actualizado correctamente.')
            else:
                messages.info(request, 'No hiciste ningún cambio.')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=usuario)

    return render(request, 'perfil.html', {'form': form})


class CambiarPasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('perfil')
    success_message = 'Contraseña cambiada correctamente.'

class ProtegerUsuarioMixin:
    """Evita que un admin se modifique a sí mismo o a un superusuario ajeno."""

    def dispatch(self, request, *args, **kwargs):
        objetivo = get_object_or_404(User, pk=kwargs['pk'])

        if objetivo == request.user:
            messages.error(request, 'No puedes modificar tu propia cuenta desde aquí. Usa tu perfil.')
            return redirect('panel_usuarios')

        if objetivo.is_superuser and not request.user.is_superuser:
            messages.error(request, 'No tienes permiso para modificar a un superusuario.')
            return redirect('panel_usuarios')

        return super().dispatch(request, *args, **kwargs)


class UsuarioLista(AdminRequeridoMixin, ListView):
    model = User
    template_name = 'gestion/lista.html'
    context_object_name = 'usuarios'
    ordering = ['-date_joined']

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(username__icontains=q) |
                Q(email__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '').strip()
        return context


class UsuarioEditar(AdminRequeridoMixin, ProtegerUsuarioMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UsuarioAdminForm
    template_name = 'gestion/form.html'
    context_object_name = 'usuario'
    success_url = reverse_lazy('panel_usuarios')
    success_message = 'Usuario actualizado correctamente.'


class UsuarioEliminar(AdminRequeridoMixin, ProtegerUsuarioMixin, DeleteView):
    model = User
    template_name = 'gestion/confirmar_eliminar.html'
    context_object_name = 'usuario'
    success_url = reverse_lazy('panel_usuarios')

    def form_valid(self, form):
        messages.success(self.request, 'Usuario eliminado.')
        return super().form_valid(form)

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensaje enviado. ¡Gracias por escribirnos!')
            return redirect('contacto')
    else:
        inicial = {}
        if request.user.is_authenticated:
            inicial = {
                'nombre': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
            }
        form = ContactoForm(initial=inicial)

    return render(request, 'contacto.html', {'form': form})


class MensajeLista(AdminRequeridoMixin, ListView):
    model = MensajeContacto
    template_name = 'gestion/mensajes.html'
    context_object_name = 'mensajes'


class MensajeEliminar(AdminRequeridoMixin, View):
    def post(self, request, pk):
        get_object_or_404(MensajeContacto, pk=pk).delete()
        messages.success(request, 'Mensaje eliminado.')
        return redirect('panel_mensajes')