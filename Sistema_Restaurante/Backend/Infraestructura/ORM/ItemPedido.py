from django.db import models
from django.core.validators import MinValueValidator
from .Menu import Menu
from .Pedido import Pedido

class ItemPedido(models.Model):
    """
    Modelo para representar los ítems individuales dentro de un pedido.
    """
    ESTADOS_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('en_preparacion', 'En Preparación'),
        ('listo', 'Listo'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    )
    
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.FloatField(validators=[MinValueValidator(0.0)])
    subtotal = models.FloatField(validators=[MinValueValidator(0.0)])
    personalizaciones = models.JSONField(default=dict, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS_CHOICES, default='pendiente')
    
    class Meta:
        db_table = 'item_pedido'
        
    def __str__(self):
        return f"{self.cantidad} x {self.menu.nombre} (Pedido #{self.pedido.id})"
    
    def save(self, *args, **kwargs):
        # Asegurar que el precio unitario es correcto al guardar
        if not self.precio_unitario:
            self.precio_unitario = self.menu.precio
            
        # Calcular el subtotal
        self.subtotal = self.precio_unitario * self.cantidad
        
        super().save(*args, **kwargs)
        
        # Actualizar el total del pedido
        self.pedido.calcular_total()
    
    def cambiar_estado(self, nuevo_estado):
        """Cambia el estado del ítem de pedido"""
        estados_validos = {
            'pendiente': ['en_preparacion', 'cancelado'],
            'en_preparacion': ['listo', 'cancelado'],
            'listo': ['entregado', 'cancelado'],
            'entregado': ['cancelado'],
            'cancelado': []
        }
        
        if nuevo_estado in estados_validos.get(self.estado, []):
            self.estado = nuevo_estado
            self.save(update_fields=['estado'])
            return True
        return False
