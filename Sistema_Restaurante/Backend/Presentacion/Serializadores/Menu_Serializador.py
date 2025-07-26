from rest_framework import serializers
from decimal import Decimal
from typing import Dict, Any


class MenuSerializador(serializers.Serializer):
    """
    Serializador para mostrar información completa de un menú.
    """
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=200)
    descripcion = serializers.CharField()
    precio = serializers.DecimalField(max_digits=10, decimal_places=2)
    categoria = serializers.CharField(max_length=100, allow_blank=True)
    tipo = serializers.CharField(max_length=100, allow_blank=True)
    imagen = serializers.URLField(allow_blank=True, required=False)
    disponible = serializers.BooleanField()
    tiempo_preparacion = serializers.IntegerField()
    veces_ordenado = serializers.IntegerField(read_only=True)
    fecha_creacion = serializers.DateTimeField(read_only=True)
    fecha_actualizacion = serializers.DateTimeField(read_only=True)
    ingredientes = serializers.ListField(
        child=serializers.DictField(),
        read_only=True
    )


class MenuCrearSerializador(serializers.Serializer):
    """
    Serializador para crear un nuevo menú.
    """
    nombre = serializers.CharField(
        max_length=200,
        help_text="Nombre del menú"
    )
    descripcion = serializers.CharField(
        help_text="Descripción detallada del menú"
    )
    precio = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2,
        min_value=Decimal('0.01'),
        help_text="Precio del menú en pesos chilenos"
    )
    categoria = serializers.CharField(
        max_length=100,
        allow_blank=True,
        required=False,
        help_text="Categoría del menú (ej: entrada, plato principal, postre)"
    )
    tipo = serializers.CharField(
        max_length=100,
        allow_blank=True,
        required=False,
        help_text="Tipo del menú (ej: vegetariano, vegano, sin gluten)"
    )
    imagen = serializers.URLField(
        allow_blank=True,
        required=False,
        help_text="URL de la imagen del menú"
    )
    tiempo_preparacion = serializers.IntegerField(
        min_value=1,
        default=15,
        help_text="Tiempo de preparación en minutos"
    )
    
    def validate_nombre(self, value):
        """Valida el nombre del menú."""
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "El nombre del menú debe tener al menos 2 caracteres"
            )
        return value.strip()
    
    def validate_descripcion(self, value):
        """Valida la descripción del menú."""
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "La descripción debe tener al menos 5 caracteres"
            )
        return value.strip()


class MenuActualizarSerializador(serializers.Serializer):
    """
    Serializador para actualizar un menú existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    nombre = serializers.CharField(
        max_length=200,
        required=False,
        help_text="Nombre del menú"
    )
    descripcion = serializers.CharField(
        required=False,
        help_text="Descripción detallada del menú"
    )
    precio = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2,
        min_value=Decimal('0.01'),
        required=False,
        help_text="Precio del menú en pesos chilenos"
    )
    categoria = serializers.CharField(
        max_length=100,
        allow_blank=True,
        required=False,
        help_text="Categoría del menú"
    )
    tipo = serializers.CharField(
        max_length=100,
        allow_blank=True,
        required=False,
        help_text="Tipo del menú"
    )
    imagen = serializers.URLField(
        allow_blank=True,
        required=False,
        help_text="URL de la imagen del menú"
    )
    disponible = serializers.BooleanField(
        required=False,
        help_text="Indica si el menú está disponible"
    )
    tiempo_preparacion = serializers.IntegerField(
        min_value=1,
        required=False,
        help_text="Tiempo de preparación en minutos"
    )
    
    def validate_nombre(self, value):
        """Valida el nombre del menú."""
        if value and len(value.strip()) < 2:
            raise serializers.ValidationError(
                "El nombre del menú debe tener al menos 2 caracteres"
            )
        return value.strip() if value else value
    
    def validate_descripcion(self, value):
        """Valida la descripción del menú."""
        if value and len(value.strip()) < 5:
            raise serializers.ValidationError(
                "La descripción debe tener al menos 5 caracteres"
            )
        return value.strip() if value else value


class MenuBusquedaSerializador(serializers.Serializer):
    """
    Serializador para criterios de búsqueda de menús.
    """
    texto = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        help_text="Texto a buscar en nombre o descripción"
    )
    categoria = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="Categoría específica"
    )
    tipo = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="Tipo específico"
    )
    precio_min = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        min_value=Decimal('0.00'),
        help_text="Precio mínimo"
    )
    precio_max = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        min_value=Decimal('0.01'),
        help_text="Precio máximo"
    )
    disponible = serializers.BooleanField(
        required=False,
        help_text="Filtrar por disponibilidad"
    )
    con_ingrediente = serializers.IntegerField(
        required=False,
        min_value=1,
        help_text="ID del ingrediente que debe contener"
    )
    
    def validate(self, data):
        """Validaciones a nivel del serializador."""
        precio_min = data.get('precio_min')
        precio_max = data.get('precio_max')
        
        if precio_min and precio_max and precio_min > precio_max:
            raise serializers.ValidationError(
                "El precio mínimo no puede ser mayor al precio máximo"
            )
        
        return data


class MenuListaSerializador(serializers.Serializer):
    """
    Serializador para listas de menús con información resumida.
    """
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    precio = serializers.DecimalField(max_digits=10, decimal_places=2)
    categoria = serializers.CharField()
    disponible = serializers.BooleanField()
    imagen = serializers.URLField(allow_blank=True)


class MenuIngredienteSerializador(serializers.Serializer):
    """
    Serializador para la relación menú-ingrediente.
    """
    ingrediente_id = serializers.IntegerField()
    ingrediente_nombre = serializers.CharField(read_only=True)
    cantidad = serializers.DecimalField(max_digits=10, decimal_places=2)
    unidad = serializers.CharField(read_only=True)


class MenuEstadisticasSerializador(serializers.Serializer):
    """
    Serializador para estadísticas de menús.
    """
    total_menus = serializers.IntegerField()
    menus_disponibles = serializers.IntegerField()
    menus_no_disponibles = serializers.IntegerField()
    por_categoria = serializers.DictField()
    por_tipo = serializers.DictField()
    precio_promedio = serializers.DecimalField(max_digits=10, decimal_places=2)
    precio_minimo = serializers.DecimalField(max_digits=10, decimal_places=2)
    precio_maximo = serializers.DecimalField(max_digits=10, decimal_places=2)


class MenuDisponibilidadSerializador(serializers.Serializer):
    """
    Serializador para el estado de disponibilidad de un menú.
    """
    menu_id = serializers.IntegerField()
    menu_nombre = serializers.CharField()
    disponible = serializers.BooleanField()
    razon_no_disponible = serializers.CharField(allow_null=True)
    ingredientes_faltantes = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )
