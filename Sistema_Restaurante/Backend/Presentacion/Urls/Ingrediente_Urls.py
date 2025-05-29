from django.urls import path
from rest_framework.routers import DefaultRouter
from Backend.Presentacion.Controladores.Ingrediente_Controlador import IngredienteViewSet

# Este archivo queda obsoleto: la gestión de rutas de ingredientes se centraliza en Presentacion/urls.py
# Si necesitas endpoints personalizados, agrégalos allí.
urlpatterns = []