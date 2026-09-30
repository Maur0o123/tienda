from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from productos.models import Producto
from .cart import Carrito


def _destino(request):
    """Vuelve a la página de origen, solo si es una URL de este mismo sitio."""
    destino = request.POST.get('next', '')
    if destino and url_has_allowed_host_and_scheme(
        destino, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return destino
    return 'home'


def ver(request):
    productos = Carrito(request).productos()
    total = sum(p.precio_final for p in productos)
    ahorro = sum(p.precio - p.precio_final for p in productos)
    return render(request, 'carrito/carrito.html', {
        'productos': productos,
        'total': total,
        'ahorro': ahorro,
    })


@require_POST
def agregar(request, pk):
    producto = get_object_or_404(Producto, pk=pk, activo=True)
    if Carrito(request).agregar(producto):
        messages.success(request, f'«{producto.nombre}» se agregó al carrito.')
    else:
        messages.info(request, 'Ese producto ya está en tu carrito.')
    return redirect(_destino(request))


@require_POST
def quitar(request, pk):
    Carrito(request).quitar(pk)
    messages.info(request, 'Producto quitado del carrito.')
    return redirect('carrito')


@require_POST
def vaciar(request):
    Carrito(request).vaciar()
    messages.info(request, 'Carrito vaciado.')
    return redirect('carrito')