def contador_carrito(request):
    return {'carrito_cantidad': len(request.session.get('carrito', []))}