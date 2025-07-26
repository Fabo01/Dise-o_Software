from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class MenuModelo(models.Model):
    """
    Modelo ORM para la tabla Menú.
    Representa la estructura de base de datos para los menús del restaurante.
    """
    
    # Campos básicos
    nombre = models.CharField(
        max_length=200, 
        verbose_name="Nombre",
        help_text="Nombre del menú"
    )
    descripcion = models.TextField(
        blank=True, 
        verbose_name="Descripción",
        help_text="Descripción detallada del menú"
    )
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Precio",
        help_text="Precio del menú en pesos chilenos"
    )
    
    # Clasificación y categorización
    categoria = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Categoría",
        help_text="Categoría del menú (ej: entrada, plato principal, postre)"
    )
    tipo = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Tipo",
        help_text="Tipo específico del menú (ej: vegetariano, vegano, sin gluten)"
    )
    
    # Estado y disponibilidad
    disponible = models.BooleanField(
        default=True, 
        verbose_name="Disponible",
        help_text="Indica si el menú está disponible para ordenar"
    )
    
    # Información adicional
    imagen = models.URLField(
        blank=True,
        null=True,
        verbose_name="Imagen",
        help_text="URL de la imagen del menú"
    )
    
    # Ingredientes (relación many-to-many)
    ingredientes = models.ManyToManyField(
        'Infraestructura.IngredienteModelo',
        blank=True,
        verbose_name="Ingredientes",
        help_text="Ingredientes necesarios para preparar este menú"
    )
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de Creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True, 
        verbose_name="Fecha de Última Actualización"
    )
    
    # Metadatos de popularidad
    veces_ordenado = models.PositiveIntegerField(
        default=0,
        verbose_name="Veces Ordenado",
        help_text="Número de veces que se ha ordenado este menú"
    )
    
    # Tiempo estimado de preparación (en minutos)
    tiempo_preparacion = models.PositiveIntegerField(
        default=15,
        verbose_name="Tiempo de Preparación",
        help_text="Tiempo estimado de preparación en minutos"
    )
    
    class Meta:
        verbose_name = "Menú"
        verbose_name_plural = "Menús"
        db_table = "menu"
        ordering = ["categoria", "nombre"]
        indexes = [
            models.Index(fields=['categoria']),
            models.Index(fields=['disponible']),
            models.Index(fields=['precio']),
            models.Index(fields=['-veces_ordenado']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(precio__gt=0),
                name='precio_positivo'
            ),
            models.CheckConstraint(
                check=models.Q(tiempo_preparacion__gt=0),
                name='tiempo_preparacion_positivo'
            )
        ]

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
    
    def incrementar_orden(self):
        """Incrementa el contador de veces ordenado."""
        self.veces_ordenado += 1
        self.save(update_fields=['veces_ordenado'])
