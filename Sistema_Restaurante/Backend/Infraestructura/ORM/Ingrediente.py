from django.db import models
from django.core.validators import MinValueValidator

class Ingrediente(models.Model):
    """
    Modelo para representar los ingredientes utilizados en los menús del restaurante.
    """
    ESTADOS_CHOICES = (
        ('disponible', 'Disponible'),
        ('agotado', 'Agotado'),
        ('descontinuado', 'Descontinuado'),
    )
    
    nombre = models.CharField(max_length=100, unique=True)
    categoria = models.CharField(max_length=50)
    cantidad = models.FloatField(validators=[MinValueValidator(0.0)])
    unidad = models.CharField(max_length=20)
    nivel_critico = models.FloatField(validators=[MinValueValidator(0.0)])
    codigo_barras = models.CharField(max_length=30, blank=True, null=True)
    imagen = models.ImageField(upload_to='ingredientes/', blank=True, null=True)
    proveedor_id = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=15, choices=ESTADOS_CHOICES, default='disponible')
    
    class Meta:
        db_table = 'ingrediente'
        ordering = ['nombre']
        
    def __str__(self):
        return f"{self.nombre} ({self.cantidad} {self.unidad})"
    
    def esta_bajo_nivel_critico(self):
        """Verifica si el ingrediente está por debajo de su nivel crítico"""
        return self.cantidad <= self.nivel_critico
    
    def actualizar_stock(self, cantidad):
        """Actualiza el stock del ingrediente"""
        nueva_cantidad = self.cantidad + cantidad
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self.cantidad = nueva_cantidad
        
        # Actualizar estado automáticamente
        if self.cantidad <= 0:
            self.estado = 'agotado'
        elif self.estado == 'agotado' and self.cantidad > 0:
            self.estado = 'disponible'
        
        self.save()
        return self.cantidad
