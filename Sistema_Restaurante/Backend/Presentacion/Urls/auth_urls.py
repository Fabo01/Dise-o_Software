"""
URLs para autenticación JWT
"""

from django.urls import path
from Backend.Presentacion.Controladores.Auth_Controlador import (
    LoginView,
    LogoutView,
    PerfilUsuarioView,
    RefreshTokenView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil-usuario'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh-token'),
]
