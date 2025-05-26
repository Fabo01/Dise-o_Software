from django.contrib import admin
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo
from Backend.Infraestructura.Modelos.Usuario_Modelo import UsuarioModelo

admin.site.register(ClienteModelo)
admin.site.register(UsuarioModelo)
admin.site.register(IngredienteModelo)