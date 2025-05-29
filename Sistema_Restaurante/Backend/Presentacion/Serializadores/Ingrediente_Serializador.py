from rest_framework import serializers
from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo

class IngredienteSerializador(serializers.ModelSerializer):
    class Meta:
        model = IngredienteModelo
        fields = [
            'id', 'nombre', 'cantidad', 'categoria', 'imagen', 'unidad_medida',
            'fecha_vencimiento', 'estado', 'fecha_registro', 'nivel_critico', 'tipo'
        ]
