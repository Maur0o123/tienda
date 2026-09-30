def contador_carrito(request):
    datos = request.session.get('carrito', {})
    cantidad = len(datos) if isinstance(datos, list) else sum(datos.values())
    return {'carrito_cantidad': cantidad}