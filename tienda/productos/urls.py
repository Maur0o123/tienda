from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductoLista.as_view(), name='panel_productos'),
    path('nuevo/', views.ProductoCrear.as_view(), name='producto_crear'),
    path('<int:pk>/editar/', views.ProductoEditar.as_view(), name='producto_editar'),
    path('<int:pk>/eliminar/', views.ProductoEliminar.as_view(), name='producto_eliminar'),
]