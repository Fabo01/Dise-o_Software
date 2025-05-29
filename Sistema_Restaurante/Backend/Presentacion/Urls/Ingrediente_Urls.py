from django.urls import path
from rest_framework.routers import DefaultRouter
from Backend.Presentacion.Controladores.Ingrediente_Controlador import IngredienteViewSet

router = DefaultRouter()
router.register(r'ingredientes', IngredienteViewSet, basename='ingrediente')

urlpatterns = router.urls