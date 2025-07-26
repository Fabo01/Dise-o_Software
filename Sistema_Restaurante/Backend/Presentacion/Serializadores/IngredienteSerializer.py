"""
Serializador para el modelo Ingrediente
Convierte entre objetos Ingrediente y representaciones JSON
"""
from rest_framework import serializers
from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo


class IngredienteSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo IngredienteModelo
    Maneja la serialización y deserialización de datos de ingrediente
    """
    
    # Campos calculados
    stock_estado = serializers.SerializerMethodField()
    dias_restantes = serializers.SerializerMethodField()
    
    class Meta:
        model = IngredienteModelo
        fields = [
            'id',
            'nombre',
            'cantidad',
            'unidad_medida',
            'categoria',
            'imagen',
            'nivel_critico',
            'fecha_vencimiento',
            'estado',
            'fecha_registro',
            'tipo',
            'stock_estado',
            'dias_restantes'
        ]
        read_only_fields = ['fecha_registro']
    
    def get_stock_estado(self, obj):
        """Determinar el estado del stock"""
        if obj.cantidad <= 0:
            return 'agotado'
        elif obj.cantidad <= obj.nivel_critico:
            return 'critico'
        elif obj.cantidad <= (obj.nivel_critico * 2):
            return 'bajo'
        else:
            return 'normal'
    
    def get_dias_restantes(self, obj):
        """Calcular días restantes hasta vencimiento"""
        if obj.fecha_vencimiento:
            from django.utils import timezone
            dias = (obj.fecha_vencimiento - timezone.now().date()).days
            return max(0, dias)
        return None
    
    def validate_cantidad(self, value):
        """Validar que la cantidad sea positiva"""
        if value < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa.")
        return value
    
    def validate_nivel_critico(self, value):
        """Validar que el nivel crítico sea positivo"""
        if value < 0:
            raise serializers.ValidationError("El nivel crítico no puede ser negativo.")
        return value
    
    def validate_precio_unitario(self, value):
        """Validar que el precio sea positivo"""
        if value < 0:
            raise serializers.ValidationError("El precio unitario no puede ser negativo.")
        return value
    
    def validate(self, attrs):
        """Validaciones a nivel de objeto"""
        cantidad = attrs.get('cantidad')
        nivel_critico = attrs.get('nivel_critico')
        
        # Si estamos actualizando, obtener valores actuales si no se proporcionan
        if self.instance:
            cantidad = cantidad if cantidad is not None else self.instance.cantidad
            nivel_critico = nivel_critico if nivel_critico is not None else self.instance.nivel_critico
        
        # Validar que el nivel crítico sea lógico comparado con la cantidad actual
        if nivel_critico and cantidad is not None and nivel_critico > cantidad * 10:
            raise serializers.ValidationError({
                'nivel_critico': 'El nivel crítico parece demasiado alto comparado con la cantidad actual.'
            })
        
        return attrs
    
    def to_representation(self, instance):
        """Personalizar la representación de salida"""
        data = super().to_representation(instance)
        
        # Formatear fechas
        if instance.fecha_creacion:
            data['fecha_creacion'] = instance.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')
        if instance.fecha_actualizacion:
            data['fecha_actualizacion'] = instance.fecha_actualizacion.strftime('%Y-%m-%d %H:%M:%S')
        if instance.fecha_vencimiento:
            data['fecha_vencimiento'] = instance.fecha_vencimiento.strftime('%Y-%m-%d')
        
        # Agregar alertas si es necesario
        alertas = []
        
        if instance.cantidad <= 0:
            alertas.append('Sin stock disponible')
        elif instance.cantidad <= instance.nivel_critico:
            alertas.append('Stock en nivel crítico')
        
        if instance.fecha_vencimiento:
            from django.utils import timezone
            dias_vencimiento = (instance.fecha_vencimiento - timezone.now().date()).days
            if dias_vencimiento <= 0:
                alertas.append('Producto vencido')
            elif dias_vencimiento <= 7:
                alertas.append(f'Vence en {dias_vencimiento} días')
        
        data['alertas'] = alertas
        
        return data


class IngredienteCreateSerializer(IngredienteSerializer):
    """
    Serializador específico para creación de ingredientes
    """
    
    def validate_nombre(self, value):
        """Validar que el nombre sea único"""
        if IngredienteModelo.objects.filter(nombre__iexact=value).exists():
            raise serializers.ValidationError("Ya existe un ingrediente con este nombre.")
        return value


class IngredienteListSerializer(serializers.ModelSerializer):
    """
    Serializador simplificado para listado de ingredientes
    Solo incluye campos esenciales para mejorar performance
    """
    
    stock_estado = serializers.SerializerMethodField()
    
    class Meta:
        model = IngredienteModelo
        fields = [
            'id',
            'nombre',
            'cantidad',
            'unidad_medida',
            'categoria',
            'nivel_critico',
            'activo',
            'stock_estado'
        ]
    
    def get_stock_estado(self, obj):
        """Determinar el estado del stock"""
        if obj.cantidad <= 0:
            return 'agotado'
        elif obj.cantidad <= obj.nivel_critico:
            return 'critico'
        elif obj.cantidad <= (obj.nivel_critico * 2):
            return 'bajo'
        else:
            return 'normal'


class IngredienteStockSerializer(serializers.ModelSerializer):
    """
    Serializador específico para operaciones de stock
    """
    
    class Meta:
        model = IngredienteModelo
        fields = [
            'id',
            'nombre',
            'cantidad',
            'unidad_medida',
            'nivel_critico'
        ]
        read_only_fields = ['id', 'nombre', 'unidad_medida', 'nivel_critico']


class IngredienteUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador para actualización de ingredientes
    Excluye campos que no deberían modificarse frecuentemente
    """
    
    class Meta:
        model = IngredienteModelo
        fields = [
            'descripcion',
            'cantidad',
            'precio_unitario',
            'proveedor',
            'nivel_critico',
            'fecha_vencimiento',
            'activo'
        ]
    
    def validate_nombre(self, value):
        """Validar que el nombre sea único (excepto para el ingrediente actual)"""
        if self.instance:
            if IngredienteModelo.objects.filter(nombre__iexact=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Ya existe un ingrediente con este nombre.")
        return value
