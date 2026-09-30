from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.catalogo, name='catalogo'),
    path('ofertas/', views.catalogo, {'solo_ofertas': True}, name='ofertas'),
]