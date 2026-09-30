from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver, name='carrito'),
    path('agregar/<int:pk>/', views.agregar, name='carrito_agregar'),
    path('quitar/<int:pk>/', views.quitar, name='carrito_quitar'),
    path('vaciar/', views.vaciar, name='carrito_vaciar'),
]