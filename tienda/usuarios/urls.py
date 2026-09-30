from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/password/', views.CambiarPasswordView.as_view(), name='password_change'),
    path('panel/usuarios/', views.UsuarioLista.as_view(), name='panel_usuarios'),
    path('panel/usuarios/<int:pk>/editar/', views.UsuarioEditar.as_view(), name='usuario_editar'),
    path('panel/usuarios/<int:pk>/eliminar/', views.UsuarioEliminar.as_view(), name='usuario_eliminar'),
    path('contacto/', views.contacto, name='contacto'),
    path('terminos/', TemplateView.as_view(template_name='terminos.html'), name='terminos'),
    path('privacidad/', TemplateView.as_view(template_name='privacidad.html'), name='privacidad'),
    path('panel/mensajes/', views.MensajeLista.as_view(), name='panel_mensajes'),
    path('panel/mensajes/<int:pk>/eliminar/', views.MensajeEliminar.as_view(), name='mensaje_eliminar'),
]