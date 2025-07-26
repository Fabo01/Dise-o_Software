"""
Serializadores para la gestión de Mesas.
Define la serialización y validación de datos para los endpoints de mesas.
"""

from rest_framework import serializers
from Backend.Infraestructura.Modelos.Mesa_Modelo import MesaModelo


class MesaDTOSerializador(serializers.Serializer):
    """
    Serializador para DTOs de Mesa.
    Maneja la serialización de entidades Mesa convertidas a DTOs.
    """
    id = serializers.IntegerField()
    numero = serializers.CharField(max_length=10)
    capacidad = serializers.IntegerField()
    estado = serializers.CharField(max_length=20)
    ubicacion = serializers.CharField(max_length=100, allow_blank=True, required=False)
    caracteristicas = serializers.CharField(allow_blank=True, required=False)
    tipo_mesa = serializers.CharField(max_length=20, required=False)
    activa = serializers.BooleanField(default=True)
    fecha_creacion = serializers.DateTimeField(required=False)
    fecha_modificacion = serializers.DateTimeField(required=False)


class MesaSerializador(serializers.ModelSerializer):
    """
    Serializador principal para Mesa.
    Maneja la serialización completa de una mesa.
    """
    
    class Meta:
        model = MesaModelo
        fields = [
            'id',
            'numero',
            'capacidad',
            'estado',
            'ubicacion',
            'caracteristicas',
            'tipo_mesa',
            'activa',
            'fecha_creacion',
            'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def validate_numero(self, value):
        """Valida que el número de mesa sea único."""
        if value <= 0:
            raise serializers.ValidationError("El número de mesa debe ser mayor a 0")
        
        # Verificar unicidad (excluyendo la instancia actual en actualizaciones)
        queryset = MesaModelo.objects.filter(numero=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError("Ya existe una mesa con este número")
        
        return value
    
    def validate_capacidad(self, value):
        """Valida que la capacidad sea válida."""
        if value <= 0:
            raise serializers.ValidationError("La capacidad debe ser mayor a 0")
        if value > 20:
            raise serializers.ValidationError("La capacidad no puede ser mayor a 20 personas")
        return value
    
    def validate_estado(self, value):
        """Valida que el estado sea válido."""
        estados_validos = ['libre', 'ocupada', 'reservada', 'limpieza', 'fuera_servicio']
        if value not in estados_validos:
            raise serializers.ValidationError(
                f"Estado inválido. Estados válidos: {', '.join(estados_validos)}"
            )
        return value


class CrearMesaSerializador(serializers.ModelSerializer):
    """
    Serializador para crear una nueva mesa.
    """
    
    class Meta:
        model = MesaModelo
        fields = [
            'numero',
            'capacidad',
            'ubicacion',
            'caracteristicas',
            'tipo_mesa'
        ]
    
    def validate_numero(self, value):
        """Valida que el número de mesa sea único."""
        if value <= 0:
            raise serializers.ValidationError("El número de mesa debe ser mayor a 0")
        
        if MesaModelo.objects.filter(numero=value).exists():
            raise serializers.ValidationError("Ya existe una mesa con este número")
        
        return value
    
    def validate_capacidad(self, value):
        """Valida que la capacidad sea válida."""
        if value <= 0:
            raise serializers.ValidationError("La capacidad debe ser mayor a 0")
        if value > 20:
            raise serializers.ValidationError("La capacidad no puede ser mayor a 20 personas")
        return value
    
    def create(self, validated_data):
        """Crea una nueva mesa con estado libre por defecto."""
        validated_data['estado'] = 'libre'
        return super().create(validated_data)


class ActualizarMesaSerializador(serializers.ModelSerializer):
    """
    Serializador para actualizar una mesa existente.
    """
    
    class Meta:
        model = MesaModelo
        fields = [
            'numero',
            'capacidad',
            'ubicacion',
            'caracteristicas',
            'tipo_mesa',
            'estado'
        ]
        extra_kwargs = {
            'numero': {'required': False},
            'capacidad': {'required': False},
            'ubicacion': {'required': False},
            'caracteristicas': {'required': False},
            'tipo_mesa': {'required': False},
            'estado': {'required': False}
        }
    
    def validate_numero(self, value):
        """Valida que el número de mesa sea único."""
        if value <= 0:
            raise serializers.ValidationError("El número de mesa debe ser mayor a 0")
        
        # Excluir la instancia actual de la validación de unicidad
        queryset = MesaModelo.objects.filter(numero=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError("Ya existe una mesa con este número")
        
        return value
    
    def validate_capacidad(self, value):
        """Valida que la capacidad sea válida."""
        if value <= 0:
            raise serializers.ValidationError("La capacidad debe ser mayor a 0")
        if value > 20:
            raise serializers.ValidationError("La capacidad no puede ser mayor a 20 personas")
        return value
    
    def validate_estado(self, value):
        """Valida que el estado sea válido."""
        estados_validos = ['libre', 'ocupada', 'reservada', 'limpieza', 'fuera_servicio']
        if value not in estados_validos:
            raise serializers.ValidationError(
                f"Estado inválido. Estados válidos: {', '.join(estados_validos)}"
            )
        return value


class CambiarEstadoMesaSerializador(serializers.Serializer):
    """
    Serializador para cambiar el estado de una mesa.
    """
    
    estado = serializers.ChoiceField(
        choices=[
            ('libre', 'Libre'),
            ('ocupada', 'Ocupada'),
            ('reservada', 'Reservada'),
            ('limpieza', 'En Limpieza'),
            ('fuera_servicio', 'Fuera de Servicio')
        ]
    )
    
    def validate_estado(self, value):
        """Validación adicional del estado."""
        # Aquí se pueden agregar validaciones específicas de transición de estado
        return value


class MesaResumenSerializador(serializers.ModelSerializer):
    """
    Serializador resumido para mesa (usado en listados simples).
    """
    
    class Meta:
        model = MesaModelo
        fields = ['id', 'numero', 'capacidad', 'estado']


class MesaDisponibleSerializador(serializers.ModelSerializer):
    """
    Serializador para mesas disponibles (usado en selección de mesas).
    """
    
    class Meta:
        model = MesaModelo
        fields = ['id', 'numero', 'capacidad', 'ubicacion']
    
    def to_representation(self, instance):
        """Personaliza la representación para incluir información adicional."""
        data = super().to_representation(instance)
        data['descripcion'] = f"Mesa {instance.numero} - {instance.capacidad} personas"
        if instance.ubicacion:
            data['descripcion'] += f" ({instance.ubicacion})"
        return data


class EstadisticasMesaSerializador(serializers.Serializer):
    """
    Serializador para estadísticas de mesas.
    """
    
    total_mesas = serializers.IntegerField()
    mesas_disponibles = serializers.IntegerField()
    mesas_ocupadas = serializers.IntegerField()
    mesas_reservadas = serializers.IntegerField()
    mesas_fuera_servicio = serializers.IntegerField()
    porcentaje_ocupacion = serializers.FloatField()
    capacidad_total = serializers.IntegerField()
    capacidad_disponible = serializers.IntegerField()
