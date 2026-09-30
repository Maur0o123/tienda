from productos.models import Producto

MAX_CANTIDAD = 10


def limite_para(producto):
    """Máximo que se puede llevar: el tope por producto o el stock, lo que sea menor."""
    return min(MAX_CANTIDAD, producto.stock)


class Carrito:
    CLAVE = 'carrito'

    def __init__(self, request):
        self.session = request.session
        datos = self.session.get(self.CLAVE, {})
        if isinstance(datos, list):
            datos = {str(pk): 1 for pk in datos}
        self.items = dict(datos)
        self.avisos = []

    def _guardar(self):
        self.session[self.CLAVE] = self.items

    def cantidad(self, pk):
        return self.items.get(str(pk), 0)

    def agregar(self, producto):
        """Suma una unidad. Devuelve False si ya se alcanzó el límite o no hay stock."""
        actual = self.cantidad(producto.pk)
        if actual >= limite_para(producto):
            return False
        self.items[str(producto.pk)] = actual + 1
        self._guardar()
        return True

    def restar(self, pk):
        """Resta una unidad, sin bajar de 1 (para quitarlo del todo se usa quitar)."""
        actual = self.cantidad(pk)
        if actual > 1:
            self.items[str(pk)] = actual - 1
            self._guardar()

    def quitar(self, pk):
        if str(pk) in self.items:
            del self.items[str(pk)]
            self._guardar()

    def vaciar(self):
        self.items = {}
        self._guardar()

    def lineas(self):
        """Lista de {producto, cantidad, limite, subtotal}.

        Descarta productos eliminados u ocultos, quita los que se agotaron
        y ajusta las cantidades que superan el stock actual.
        """
        orden = list(self.items)
        productos = Producto.objects.filter(pk__in=[int(k) for k in orden], activo=True)

        lineas = []
        vigentes = {}
        for p in productos:
            cantidad = self.items[str(p.pk)]
            limite = limite_para(p)

            if limite == 0:
                self.avisos.append(f'«{p.nombre}» se agotó y se quitó de tu carrito.')
                continue
            if cantidad > limite:
                self.avisos.append(f'Ajustamos «{p.nombre}» a {limite} unidades por disponibilidad.')
                cantidad = limite

            vigentes[str(p.pk)] = cantidad
            lineas.append({
                'producto': p,
                'cantidad': cantidad,
                'limite': limite,
                'subtotal': p.precio_final * cantidad,
            })

        if vigentes != self.items:
            self.items = vigentes
            self._guardar()

        lineas.sort(key=lambda l: orden.index(str(l['producto'].pk)))
        return lineas