"""
Serializador para el modelo Pedido
Convierte entre objetos Pedido y representaciones JSON
"""
from rest_framework import serializers
from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo, ItemPedidoModelo
from Backend.Presentacion.Serializadores.ClienteSerializer import ClienteSerializer


class ItemPedidoSerializer(serializers.ModelSerializer):
    """Serializador para items de pedido"""
    
    menu_nombre = serializers.CharField(source='menu.nombre', read_only=True)
    
    class Meta:
        model = ItemPedidoModelo
        fields = [
            'id',
            'menu',
            'menu_nombre',
            'cantidad',
            'precio_unitario',
            'subtotal',
            'observaciones'
        ]
        read_only_fields = ['subtotal']


class PedidoSerializer(serializers.ModelSerializer):
    """Serializador para el modelo PedidoModelo"""
    
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    mesa_numero = serializers.CharField(source='mesa.numero', read_only=True)
    items = ItemPedidoSerializer(many=True, read_only=True)
    
    class Meta:
        model = PedidoModelo
        fields = [
            'id',
            'cliente',
            'cliente_nombre',
            'tipo_pedido',
            'estado',
            'mesa',
            'mesa_numero',
            'direccion_entrega',
            'telefono_contacto',
            'observaciones_generales',
            'total',
            'fecha_creacion',
            'fecha_confirmacion',
            'fecha_entrega',
            'tiempo_preparacion_estimado',
            'items'
        ]
        read_only_fields = ['fecha_creacion', 'total']
    
    def to_representation(self, instance):
        """Personalizar la representación de salida"""
        data = super().to_representation(instance)
        
        # Formatear fechas
        if instance.fecha_creacion:
            data['fecha_creacion'] = instance.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')
        if instance.fecha_confirmacion:
            data['fecha_confirmacion'] = instance.fecha_confirmacion.strftime('%Y-%m-%d %H:%M:%S')
        if instance.fecha_entrega:
            data['fecha_entrega'] = instance.fecha_entrega.strftime('%Y-%m-%d %H:%M:%S')
        
        # Agregar información calculada
        data['cantidad_total_items'] = instance.cantidad_total_items
        data['puede_modificar_items'] = instance.puede_modificar_items
        data['esta_atrasado'] = instance.esta_atrasado()
        
        return data


class PedidoCreateSerializer(serializers.ModelSerializer):
    """Serializador para creación de pedidos"""
    
    items_data = serializers.ListField(write_only=True, required=False)
    
    class Meta:
        model = PedidoModelo
        fields = [
            'cliente',
            'tipo_pedido',
            'mesa',
            'direccion_entrega',
            'telefono_contacto',
            'observaciones_generales',
            'tiempo_preparacion_estimado',
            'items_data'
        ]
    
    def validate(self, attrs):
        """Validaciones a nivel de objeto"""
        tipo_pedido = attrs.get('tipo_pedido')
        
        # Validar que un pedido de mesa tenga mesa asignada
        if tipo_pedido == 'mesa' and not attrs.get('mesa'):
            raise serializers.ValidationError({
                'mesa': 'Un pedido de mesa debe tener una mesa asignada.'
            })
        
        # Validar que un pedido de delivery tenga dirección
        if tipo_pedido == 'delivery' and not attrs.get('direccion_entrega'):
            raise serializers.ValidationError({
                'direccion_entrega': 'Un pedido de delivery debe tener dirección de entrega.'
            })
        
        return attrs
    
    def create(self, validated_data):
        """Crear pedido con sus items"""
        items_data = validated_data.pop('items_data', [])
        
        # Crear el pedido
        pedido = PedidoModelo.objects.create(**validated_data)
        
        # Crear los items del pedido
        for item_data in items_data:
            ItemPedidoModelo.objects.create(
                pedido=pedido,
                **item_data
            )
        
        return pedido


class PedidoListSerializer(serializers.ModelSerializer):
    """Serializador simplificado para listado de pedidos"""
    
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    mesa_numero = serializers.CharField(source='mesa.numero', read_only=True)
    cantidad_items = serializers.SerializerMethodField()
    
    class Meta:
        model = PedidoModelo
        fields = [
            'id',
            'cliente_nombre',
            'tipo_pedido',
            'estado',
            'mesa_numero',
            'total',
            'fecha_creacion',
            'cantidad_items'
        ]
    
    def get_cantidad_items(self, obj):
        """Obtener la cantidad total de items"""
        return obj.cantidad_total_items
    
    def to_representation(self, instance):
        """Personalizar la representación de salida"""
        data = super().to_representation(instance)
        
        # Formatear fecha
        if instance.fecha_creacion:
            data['fecha_creacion'] = instance.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')
        
        return data


class PedidoUpdateSerializer(serializers.ModelSerializer):
    """Serializador para actualización de pedidos"""
    
    class Meta:
        model = PedidoModelo
        fields = [
            'estado',
            'mesa',
            'direccion_entrega',
            'telefono_contacto',
            'observaciones_generales',
            'fecha_confirmacion',
            'fecha_entrega',
            'tiempo_preparacion_estimado'
        ]
    
    def validate_estado(self, value):
        """Validar transiciones de estado"""
        if self.instance:
            estado_actual = self.instance.estado
            
            # Definir transiciones válidas
            transiciones_validas = {
                'pendiente': ['confirmado', 'cancelado'],
                'confirmado': ['en_preparacion', 'cancelado'],
                'en_preparacion': ['listo', 'cancelado'],
                'listo': ['entregado'],
                'entregado': [],  # Estado final
                'cancelado': []   # Estado final
            }
            
            if value not in transiciones_validas.get(estado_actual, []):
                raise serializers.ValidationError(
                    f"No se puede cambiar de '{estado_actual}' a '{value}'"
                )
        
        return value
