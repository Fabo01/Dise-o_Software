from rest_framework import serializers

class ClienteSerializador(serializers.Serializer):
    """
    Serializador para la entidad Cliente.
    Convierte objetos Cliente a JSON y viceversa.
    """

    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100, required=True)
    rut = serializers.CharField(max_length=12, required=True)
    correo = serializers.EmailField(required=True, allow_blank=False)
    telefono = serializers.CharField(max_length=15, required=False, allow_blank=True)
    direccion = serializers.CharField(max_length=200, required=False, allow_blank=True)
    estado = serializers.CharField(read_only=True)
    fecha_registro = serializers.DateTimeField(read_only=True)
    ultima_visita = serializers.DateTimeField(read_only=True)


    class Meta:
        model = 'Cliente'
        fields = '__all__'
        
    def to_representation(self, instance):
        """
        Convierte una entidad Cliente a un diccionario para serialización
        """
        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'rut': instance.rut,
            'correo': str(instance.correo),  # Convertir CorreoVO a cadena
            'telefono': instance.telefono or '',
            'direccion': instance.direccion or '',
            'estado': instance.estado,
            'fecha_registro': instance.fecha_registro,
            'ultima_visita': instance.ultima_visita
        }