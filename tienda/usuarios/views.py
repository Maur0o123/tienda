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