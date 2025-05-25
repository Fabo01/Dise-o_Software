from django.contrib import admin
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo

admin.site.register(ClienteModelo)
admin.site.register(IngredienteModelo)