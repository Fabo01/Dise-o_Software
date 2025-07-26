"""
Serializador para el modelo Cliente
Convierte entre objetos Cliente y representaciones JSON
"""
from rest_framework import serializers
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo


class ClienteSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo ClienteModelo
    Maneja la serialización y deserialización de datos de cliente
    """
    
    class Meta:
        model = ClienteModelo
        fields = [
            'rut',
            'nombre', 
            'correo',
            'telefono',
            'direccion',
            'fecha_registro'
        ]
        read_only_fields = ['fecha_registro']
    
    def validate_rut(self, value):
        """Validar formato del RUT"""
        # La validación del RUT ya se hace en el modelo
        # Aquí podemos agregar validaciones adicionales si es necesario
        return value
    
    def validate_correo(self, value):
        """Validar que el correo sea único (excepto para actualizaciones)"""
        if self.instance:
            # Es una actualización, excluir el cliente actual
            if ClienteModelo.objects.filter(correo=value).exclude(rut=self.instance.rut).exists():
                raise serializers.ValidationError("Ya existe un cliente con este correo electrónico.")
        else:
            # Es una creación, verificar que no exista
            if ClienteModelo.objects.filter(correo=value).exists():
                raise serializers.ValidationError("Ya existe un cliente con este correo electrónico.")
        return value
    
    def to_representation(self, instance):
        """Personalizar la representación de salida"""
        data = super().to_representation(instance)
        # Formatear fecha de registro
        if instance.fecha_registro:
            data['fecha_registro'] = instance.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
        return data


class ClienteCreateSerializer(ClienteSerializer):
    """
    Serializador específico para creación de clientes
    Incluye validaciones adicionales para nuevos clientes
    """
    
    def validate(self, attrs):
        """Validaciones a nivel de objeto"""
        # Verificar que el RUT no esté ya registrado
        if ClienteModelo.objects.filter(rut=attrs['rut']).exists():
            raise serializers.ValidationError({
                'rut': 'Ya existe un cliente con este RUT.'
            })
        return attrs


class ClienteListSerializer(serializers.ModelSerializer):
    """
    Serializador simplificado para listado de clientes
    Solo incluye campos esenciales para mejorar performance
    """
    
    total_pedidos = serializers.SerializerMethodField()
    
    class Meta:
        model = ClienteModelo
        fields = [
            'rut',
            'nombre',
            'correo',
            'telefono',
            'total_pedidos'
        ]
    
    def get_total_pedidos(self, obj):
        """Obtener el número total de pedidos del cliente"""
        return obj.pedidos.count()


class ClienteDetailSerializer(ClienteSerializer):
    """
    Serializador detallado para vista individual de cliente
    Incluye información adicional y relaciones
    """
    
    pedidos_recientes = serializers.SerializerMethodField()
    total_pedidos = serializers.SerializerMethodField()
    ultimo_pedido = serializers.SerializerMethodField()
    
    class Meta(ClienteSerializer.Meta):
        fields = ClienteSerializer.Meta.fields + [
            'pedidos_recientes',
            'total_pedidos',
            'ultimo_pedido'
        ]
    
    def get_pedidos_recientes(self, obj):
        """Obtener los últimos 5 pedidos del cliente"""
        pedidos = obj.pedidos.all().order_by('-fecha_creacion')[:5]
        return [{
            'id': pedido.id,
            'fecha_creacion': pedido.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
            'estado': pedido.estado,
            'total': str(pedido.total),
            'tipo_pedido': pedido.tipo_pedido
        } for pedido in pedidos]
    
    def get_total_pedidos(self, obj):
        """Obtener el número total de pedidos del cliente"""
        return obj.pedidos.count()
    
    def get_ultimo_pedido(self, obj):
        """Obtener información del último pedido"""
        ultimo_pedido = obj.pedidos.order_by('-fecha_creacion').first()
        if ultimo_pedido:
            return {
                'id': ultimo_pedido.id,
                'fecha_creacion': ultimo_pedido.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
                'estado': ultimo_pedido.estado,
                'total': str(ultimo_pedido.total)
            }
        return None
