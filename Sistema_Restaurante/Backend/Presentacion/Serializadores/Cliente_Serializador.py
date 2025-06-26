from rest_framework import serializers
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo

class ClienteSerializador(serializers.ModelSerializer):
    """
    Serializador para la entidad Cliente basado en el modelo ORM.
    Convierte objetos ClienteModelo a JSON y viceversa.
    """
    rut = serializers.CharField(max_length=12, required=True)

    class Meta:
        model = ClienteModelo
        fields = '__all__'
        read_only_fields = ('ultima_visita', 'estado')  # <-- Solo lectura

    def to_representation(self, instance):
        """
        Convierte una entidad Cliente a un diccionario para serialización
        """
        data = super().to_representation(instance)
        data['correo'] = str(data.get('correo', ''))  # Asegura string
        data['telefono'] = data.get('telefono', '') or ''
        data['direccion'] = data.get('direccion', '') or ''
        data['rut'] = data.get('rut', '') or ''
        return data

    def validate_rut(self, value):
        # Aquí puedes agregar tu lógica de validación de RUT chileno
        # Por ejemplo, usando tu objeto de valor RutVO o Rut
        from Backend.Dominio.Objetos_Valor.RutVO import RutVO
        try:
            RutVO(value)
        except Exception:
            raise serializers.ValidationError("RUT inválido")
        return value