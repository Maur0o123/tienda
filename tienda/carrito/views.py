from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from productos.models import Producto
from .cart import Carrito, MAX_CANTIDAD


def _destino(request):
    """Vuelve a la página de origen, solo si es una URL de este mismo sitio."""
    destino = request.POST.get('next', '')
    if destino and url_has_allowed_host_and_scheme(
        destino, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return destino
    return 'home'


def _aviso_limite(request, producto):
    if producto.agotado:
        messages.error(request, f'«{producto.nombre}» tiene el stock agotado.')
    elif producto.stock < MAX_CANTIDAD:
        messages.info(request, f'Ya tienes en tu carrito todo el stock disponible de «{producto.nombre}».')
    else:
        messages.info(request, f'Máximo {MAX_CANTIDAD} unidades por producto.')


def ver(request):
    carrito = Carrito(request)
    lineas = carrito.lineas()

    for aviso in carrito.avisos:
        messages.warning(request, aviso)

    return render(request, 'carrito/carrito.html', {
        'lineas': lineas,
        'unidades': sum(l['cantidad'] for l in lineas),
        'total': sum(l['subtotal'] for l in lineas),
        'ahorro': sum(
            (l['producto'].precio - l['producto'].precio_final) * l['cantidad'] for l in lineas
        ),
        'max_cantidad': MAX_CANTIDAD,
    })


@require_POST
def agregar(request, pk):
    """Botón «Agregar» de las tarjetas de producto."""
    producto = get_object_or_404(Producto, pk=pk, activo=True)
    carrito = Carrito(request)
    if carrito.agregar(producto):
        messages.success(
            request,
            f'«{producto.nombre}» agregado al carrito ({carrito.cantidad(producto.pk)} en total).',
        )
    else:
        _aviso_limite(request, producto)
    return redirect(_destino(request))


@require_POST
def sumar(request, pk):
    """Botón «+» dentro del carrito."""
    producto = get_object_or_404(Producto, pk=pk, activo=True)
    if not Carrito(request).agregar(producto):
        _aviso_limite(request, producto)
    return redirect('carrito')


@require_POST
def restar(request, pk):
    """Botón «−» dentro del carrito."""
    Carrito(request).restar(pk)
    return redirect('carrito')


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