from rest_framework import serializers
from Backend.Infraestructura.Modelos.Usuario_Modelo import UsuarioModelo

class UsuarioSerializador(serializers.ModelSerializer):
    """
    Serializador para la entidad Usuario basado en el modelo ORM.
    Convierte objetos UsuarioModelo a JSON y viceversa.
    """
    class Meta:
        model = UsuarioModelo
        fields = '__all__'
        read_only_fields = ["username", "fecha_registro", "ultima_sesion"]

    def to_representation(self, instance):
        # Obtén el diccionario base
        data = super().to_representation(instance)
        # Asegura que 'email' sea una cadena
        data['email'] = str(data.get('email', ''))
        # Asegura que 'telefono' tenga un valor por defecto
        data['telefono'] = data.get('telefono', '') or ''
        return data
