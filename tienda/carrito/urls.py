from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver, name='carrito'),
    path('agregar/<int:pk>/', views.agregar, name='carrito_agregar'),
    path('sumar/<int:pk>/', views.sumar, name='carrito_sumar'),
    path('restar/<int:pk>/', views.restar, name='carrito_restar'),
    path('quitar/<int:pk>/', views.quitar, name='carrito_quitar'),
    path('vaciar/', views.vaciar, name='carrito_vaciar'),
]