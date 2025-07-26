# Backend/Infraestructura/Modelos/DetallePedido_Modelo.py
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class DetallePedidoModelo(models.Model):
    """
    Modelo que representa el detalle de un pedido.
    Cada registro representa un elemento del menú dentro de un pedido.
    """
    
    pedido = models.ForeignKey(
        'Pedido_Modelo',
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    
    menu = models.ForeignKey(
        'Menu_Modelo',
        on_delete=models.CASCADE,
        related_name='detalles_pedido'
    )
    
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Cantidad de este elemento en el pedido"
    )
    
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Precio unitario al momento del pedido"
    )
    
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Subtotal del detalle (cantidad * precio_unitario)"
    )
    
    notas_especiales = models.TextField(
        blank=True,
        null=True,
        help_text="Notas especiales para este elemento (sin cebolla, etc.)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'detalle_pedido'
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedidos'
        ordering = ['id']
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para calcular automáticamente el subtotal.
        """
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.cantidad}x {self.menu.nombre} - ${self.subtotal}"
