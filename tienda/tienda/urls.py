from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', include('productos.urls')),
    path('carrito/', include('carrito.urls')),
    path('', include('productos.urls_tienda')),
    path('', include('usuarios.urls')),
]