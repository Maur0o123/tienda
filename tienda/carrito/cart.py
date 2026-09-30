from productos.models import Producto


class Carrito:
    CLAVE = 'carrito'

    def __init__(self, request):
        self.session = request.session
        self.ids = list(self.session.get(self.CLAVE, []))

    def _guardar(self):
        self.session[self.CLAVE] = self.ids

    def agregar(self, producto):
        """Devuelve False si el producto ya estaba en el carrito."""
        if producto.pk in self.ids:
            return False
        self.ids.append(producto.pk)
        self._guardar()
        return True

    def quitar(self, pk):
        if pk in self.ids:
            self.ids.remove(pk)
            self._guardar()

    def vaciar(self):
        self.ids = []
        self._guardar()

    def productos(self):
        """Productos vigentes; descarta los que se eliminaron o ocultaron."""
        productos = list(Producto.objects.filter(pk__in=self.ids, activo=True))
        vigentes = [p.pk for p in productos]
        if len(vigentes) != len(self.ids):
            self.ids = vigentes
            self._guardar()
        return productos