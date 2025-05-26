from django.urls import path
from Backend.Presentacion.Controladores.Usuario_Controlador import UsuarioAPI   

urlpatterns = [
    #Urls para operaciones basicas de usuarios
    path('usuarios/', UsuarioAPI.as_view(), name='usuario-lista'),
    path('usuarios/<int:id>/', UsuarioAPI.as_view(), name='usuario-detalle')
]