# Backend/Infraestructura/Modelos/DeliveryRepartidor_Modelo.py
from django.db import models

class DeliveryRepartidorModelo(models.Model):
    """
    Modelo para representar repartidores de delivery
    """
    ESTADOS_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_ruta', 'En Ruta'),
        ('ocupado', 'Ocupado'),
        ('desconectado', 'Desconectado'),
    ]
    
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='disponible')
    delivery_app = models.ForeignKey(
        'Infraestructura.DeliveryAppModelo', 
        on_delete=models.CASCADE,
        related_name='repartidores',
        null=True, blank=True
    )
    vehiculo = models.CharField(max_length=50, blank=True)
    ubicacion_lat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    ubicacion_lng = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    pedido_actual = models.ForeignKey(
        'Infraestructura.DeliveryPedidoModelo',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='repartidor_actual'
    )
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'delivery_repartidor'
        verbose_name = 'Repartidor de Delivery'
        verbose_name_plural = 'Repartidores de Delivery'
    
    def __str__(self):
        return f"{self.nombre} - {self.get_estado_display()}"
    
    def esta_disponible(self):
        """Verifica si el repartidor está disponible para asignar pedidos"""
        return self.estado == 'disponible' and self.activo
