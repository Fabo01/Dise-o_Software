from rest_framework import serializers
from typing import Dict, Any, List


class ItemPedidoSerializador(serializers.Serializer):
    """Serializador para items de pedido"""
    menu_id = serializers.IntegerField(min_value=1)
    nombre_menu = serializers.CharField(max_length=200, read_only=True)
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    cantidad = serializers.IntegerField(min_value=1, max_value=50)
    observaciones = serializers.CharField(max_length=500, allow_blank=True, required=False)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)


class PedidoSerializador(serializers.Serializer):
    """Serializador principal para pedidos"""
    id = serializers.IntegerField(read_only=True)
    cliente_id = serializers.IntegerField(min_value=1)
    cliente_nombre = serializers.CharField(max_length=200, read_only=True, allow_null=True)
    cliente_rut = serializers.CharField(max_length=20, read_only=True, allow_null=True)
    
    tipo_pedido = serializers.ChoiceField(
        choices=['mesa', 'delivery', 'para_llevar'],
        default='mesa'
    )
    
    estado = serializers.ChoiceField(
        choices=['pendiente', 'confirmado', 'en_preparacion', 'listo', 'entregado', 'cancelado'],
        read_only=True
    )
    
    mesa_id = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    mesa_numero = serializers.CharField(max_length=50, read_only=True, allow_null=True)
    direccion_entrega = serializers.CharField(max_length=500, allow_blank=True, required=False)
    telefono_contacto = serializers.CharField(max_length=20, allow_blank=True, required=False)
    observaciones_generales = serializers.CharField(max_length=1000, allow_blank=True, required=False)
    
    fecha_creacion = serializers.DateTimeField(read_only=True)
    fecha_confirmacion = serializers.DateTimeField(read_only=True, allow_null=True)
    fecha_entrega = serializers.DateTimeField(read_only=True, allow_null=True)
    tiempo_preparacion_estimado = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    items = ItemPedidoSerializador(many=True)
    cantidad_total_items = serializers.IntegerField(read_only=True, allow_null=True)
    tiempo_transcurrido = serializers.IntegerField(read_only=True, allow_null=True)
    esta_atrasado = serializers.BooleanField(read_only=True, allow_null=True)

    def validate(self, data):
        """Validaciones a nivel de pedido"""
        tipo_pedido = data.get('tipo_pedido')
        mesa_id = data.get('mesa_id')
        direccion_entrega = data.get('direccion_entrega')
        
        # Validar que pedidos de mesa tengan mesa asignada
        if tipo_pedido == 'mesa' and not mesa_id:
            raise serializers.ValidationError(
                "Un pedido de mesa debe tener una mesa asignada"
            )
        
        # Validar que pedidos de delivery tengan dirección
        if tipo_pedido == 'delivery' and not direccion_entrega:
            raise serializers.ValidationError(
                "Un pedido de delivery debe tener dirección de entrega"
            )
        
        return data


class PedidoCrearSerializador(serializers.Serializer):
    """Serializador para crear nuevos pedidos"""
    cliente_id = serializers.IntegerField(min_value=1)
    
    tipo_pedido = serializers.ChoiceField(
        choices=['mesa', 'delivery', 'para_llevar'],
        default='mesa'
    )
    
    mesa_id = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    direccion_entrega = serializers.CharField(max_length=500, allow_blank=True, required=False)
    telefono_contacto = serializers.CharField(max_length=20, allow_blank=True, required=False)
    observaciones_generales = serializers.CharField(max_length=1000, allow_blank=True, required=False)
    tiempo_preparacion_estimado = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    
    items = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
        max_length=100
    )

    def validate_items(self, value):
        """Valida la lista de items del pedido"""
        for i, item in enumerate(value):
            # Validar campos requeridos
            if 'menu_id' not in item:
                raise serializers.ValidationError(f"Item {i+1}: menu_id es requerido")
            
            if 'cantidad' not in item:
                raise serializers.ValidationError(f"Item {i+1}: cantidad es requerida")
            
            if 'precio_unitario' not in item:
                raise serializers.ValidationError(f"Item {i+1}: precio_unitario es requerido")
            
            # Validar tipos y rangos
            try:
                menu_id = int(item['menu_id'])
                if menu_id < 1:
                    raise serializers.ValidationError(f"Item {i+1}: menu_id debe ser mayor a 0")
            except (ValueError, TypeError):
                raise serializers.ValidationError(f"Item {i+1}: menu_id debe ser un número entero")
            
            try:
                cantidad = int(item['cantidad'])
                if cantidad < 1 or cantidad > 50:
                    raise serializers.ValidationError(f"Item {i+1}: cantidad debe estar entre 1 y 50")
            except (ValueError, TypeError):
                raise serializers.ValidationError(f"Item {i+1}: cantidad debe ser un número entero")
            
            try:
                precio = float(item['precio_unitario'])
                if precio <= 0:
                    raise serializers.ValidationError(f"Item {i+1}: precio_unitario debe ser mayor a 0")
            except (ValueError, TypeError):
                raise serializers.ValidationError(f"Item {i+1}: precio_unitario debe ser un número")
        
        return value

    def validate(self, data):
        """Validaciones a nivel de pedido para creación"""
        tipo_pedido = data.get('tipo_pedido')
        mesa_id = data.get('mesa_id')
        direccion_entrega = data.get('direccion_entrega')
        
        # Validar que pedidos de mesa tengan mesa asignada
        if tipo_pedido == 'mesa' and not mesa_id:
            raise serializers.ValidationError(
                "Un pedido de mesa debe tener una mesa asignada"
            )
        
        # Validar que pedidos de delivery tengan dirección
        if tipo_pedido == 'delivery' and not direccion_entrega:
            raise serializers.ValidationError(
                "Un pedido de delivery debe tener dirección de entrega"
            )
        
        return data


class PedidoActualizarSerializador(serializers.Serializer):
    """Serializador para actualizar pedidos existentes"""
    tipo_pedido = serializers.ChoiceField(
        choices=['mesa', 'delivery', 'para_llevar'],
        required=False
    )
    
    mesa_id = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    direccion_entrega = serializers.CharField(max_length=500, allow_blank=True, required=False)
    telefono_contacto = serializers.CharField(max_length=20, allow_blank=True, required=False)
    observaciones_generales = serializers.CharField(max_length=1000, allow_blank=True, required=False)
    tiempo_preparacion_estimado = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    
    items = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
        max_length=100,
        required=False
    )

    def validate_items(self, value):
        """Valida la lista de items del pedido para actualización"""
        if value is not None:
            # Usar la misma validación que el serializador de creación
            crear_serializador = PedidoCrearSerializador()
            return crear_serializador.validate_items(value)
        return value


class PedidoCambiarEstadoSerializador(serializers.Serializer):
    """Serializador para cambiar el estado de un pedido"""
    nuevo_estado = serializers.ChoiceField(
        choices=['pendiente', 'confirmado', 'en_preparacion', 'listo', 'entregado', 'cancelado']
    )
    
    tiempo_preparacion = serializers.IntegerField(min_value=1, required=False)
    motivo_cancelacion = serializers.CharField(max_length=500, required=False)

    def validate(self, data):
        """Validaciones para cambio de estado"""
        nuevo_estado = data.get('nuevo_estado')
        tiempo_preparacion = data.get('tiempo_preparacion')
        motivo_cancelacion = data.get('motivo_cancelacion')
        
        # Si se confirma el pedido, se puede especificar tiempo de preparación
        if nuevo_estado == 'confirmado' and tiempo_preparacion is None:
            # No es requerido, pero se puede sugerir
            pass
        
        # Si se cancela, es recomendable dar un motivo
        if nuevo_estado == 'cancelado' and not motivo_cancelacion:
            # No es requerido, pero se puede sugerir
            pass
        
        return data


class PedidoBusquedaSerializador(serializers.Serializer):
    """Serializador para criterios de búsqueda de pedidos"""
    cliente_id = serializers.IntegerField(min_value=1, required=False)
    estado = serializers.ChoiceField(
        choices=['pendiente', 'confirmado', 'en_preparacion', 'listo', 'entregado', 'cancelado'],
        required=False
    )
    tipo_pedido = serializers.ChoiceField(
        choices=['mesa', 'delivery', 'para_llevar'],
        required=False
    )
    mesa_id = serializers.IntegerField(min_value=1, required=False)
    fecha_inicio = serializers.DateField(required=False)
    fecha_fin = serializers.DateField(required=False)
    texto = serializers.CharField(max_length=200, required=False)
    solo_activos = serializers.BooleanField(default=False)
    limite = serializers.IntegerField(min_value=1, max_value=1000, required=False)
    desplazamiento = serializers.IntegerField(min_value=0, default=0)


class PedidoResumenSerializador(serializers.Serializer):
    """Serializador para información resumida de pedidos"""
    id = serializers.IntegerField()
    cliente_nombre = serializers.CharField(max_length=200)
    tipo_pedido = serializers.CharField(max_length=20)
    estado = serializers.CharField(max_length=20)
    mesa_numero = serializers.CharField(max_length=50, allow_null=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2)
    cantidad_items = serializers.IntegerField()
    fecha_creacion = serializers.DateTimeField()
    tiempo_transcurrido = serializers.IntegerField(allow_null=True)
    esta_atrasado = serializers.BooleanField()


class PedidoEstadisticasSerializador(serializers.Serializer):
    """Serializador para estadísticas de pedidos"""
    total_pedidos = serializers.IntegerField()
    total_ventas = serializers.DecimalField(max_digits=15, decimal_places=2)
    pedidos_por_estado = serializers.DictField()
    pedidos_por_tipo = serializers.DictField()
    tiempo_promedio_preparacion = serializers.DecimalField(max_digits=8, decimal_places=2)
    pedidos_atrasados = serializers.IntegerField()
    ventas_por_fecha = serializers.DictField()


class PedidoHistorialSerializador(serializers.Serializer):
    """Serializador para historial de pedidos de un cliente"""
    cliente_id = serializers.IntegerField()
    cliente_nombre = serializers.CharField(max_length=200)
    total_pedidos = serializers.IntegerField()
    total_gastado = serializers.DecimalField(max_digits=15, decimal_places=2)
    ultimo_pedido = serializers.DateTimeField(allow_null=True)
    pedidos = PedidoResumenSerializador(many=True)


class PedidoCocinaSerializador(serializers.Serializer):
    """Serializador optimizado para mostrar pedidos en cocina"""
    id = serializers.IntegerField()
    numero_mesa = serializers.CharField(max_length=50, allow_null=True)
    tipo_pedido = serializers.CharField(max_length=20)
    estado = serializers.CharField(max_length=20)
    tiempo_transcurrido = serializers.IntegerField(allow_null=True)
    tiempo_estimado = serializers.IntegerField(allow_null=True)
    esta_atrasado = serializers.BooleanField()
    items = serializers.ListField(child=serializers.DictField())
    observaciones = serializers.CharField(max_length=1000, allow_null=True)
    prioridad = serializers.ChoiceField(choices=['alta', 'media', 'baja'])


class PedidoValidacionSerializador(serializers.Serializer):
    """Serializador para resultado de validación de pedidos"""
    es_valido = serializers.BooleanField()
    errores = serializers.ListField(child=serializers.CharField(max_length=500))
    advertencias = serializers.ListField(child=serializers.CharField(max_length=500))
    total_estimado = serializers.DecimalField(max_digits=12, decimal_places=2)
    tiempo_preparacion_total = serializers.IntegerField(allow_null=True)


class PedidoEntregaSerializador(serializers.Serializer):
    """Serializador para información de entrega de pedidos"""
    id = serializers.IntegerField()
    cliente_nombre = serializers.CharField(max_length=200)
    telefono = serializers.CharField(max_length=20, allow_null=True)
    direccion = serializers.CharField(max_length=500, allow_null=True)
    tipo_pedido = serializers.CharField(max_length=20)
    total = serializers.DecimalField(max_digits=12, decimal_places=2)
    estado = serializers.CharField(max_length=20)
    items_resumen = serializers.CharField(max_length=1000)
    tiempo_preparacion = serializers.IntegerField(allow_null=True)


class PedidoReporteSerializador(serializers.Serializer):
    """Serializador para reportes de pedidos"""
    fecha = serializers.DateField()
    total_pedidos = serializers.IntegerField()
    total_ventas = serializers.DecimalField(max_digits=15, decimal_places=2)
    pedidos_completados = serializers.IntegerField()
    pedidos_cancelados = serializers.IntegerField()
    tiempo_promedio = serializers.DecimalField(max_digits=8, decimal_places=2)
    item_mas_vendido = serializers.CharField(max_length=200, allow_null=True)
    hora_pico = serializers.CharField(max_length=20, allow_null=True)
