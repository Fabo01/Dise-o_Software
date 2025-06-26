from rest_framework import serializers
from Backend.Infraestructura.Modelos.Usuario_Modelo import UsuarioModelo

class UsuarioSerializador(serializers.ModelSerializer):
    rut = serializers.CharField(required=True)  # <-- Añade esto explícitamente

    class Meta:
        model = UsuarioModelo
        fields = ['rut', 'username', 'nombre', 'apellido', 'rol', 'email', 'telefono', 'direccion', 'password']
        # No pongas 'rut' en read_only_fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        telefono = getattr(instance, 'telefono', '')
        if hasattr(telefono, 'valor'):
            data['telefono'] = telefono.valor
        else:
            data['telefono'] = str(telefono or '')
        rut = getattr(instance, 'rut', '')
        if hasattr(rut, 'valor'):
            data['rut'] = rut.valor
        else:
            data['rut'] = str(rut or '')
        return data
