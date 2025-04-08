from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from .Cliente import Cliente
from .Menu import Menu

class Pedido(models.Model):
    """
    Modelo para representar los pedidos realizados por los clientes.
    """
    ESTADOS_CHOICES = (
        ('recibido', 'Recibido'),
        ('en_preparacion', 'En Preparación'),
        ('listo', 'Listo para servir'),
        ('entregado', 'Entregado'),
        ('pagado', 'Pagado'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )
    
    TIPOS_CHOICES = (
        ('local', 'En Local'),
        ('delivery', 'Delivery'),
        ('para_llevar', 'Para Llevar'),
    )
    
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    mesa_id = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(default=timezone.now)
    total = models.FloatField(validators=[MinValueValidator(0.0)], default=0)
    estado = models.CharField(max_length=15, choices=ESTADOS_CHOICES, default='recibido')
    notas = models.TextField(blank=True, null=True)
    creado_por = models.IntegerField(blank=True, null=True)  # FK a usuario
    tipo = models.CharField(max_length=15, choices=TIPOS_CHOICES, default='local')
    menus = models.ManyToManyField(Menu, through='ItemPedido')
    
    class Meta:
        db_table = 'pedido'
        ordering = ['-fecha']
        
    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre} ({self.fecha.strftime('%d/%m/%Y %H:%M')})"
    
    def calcular_total(self):
        """Calcula el total del pedido basado en sus ítems"""
        total = 0
        for item in self.itempedido_set.all():
            total += item.subtotal
        
        self.total = total
        self.save(update_fields=['total'])
        return self.total
    
    def cambiar_estado(self, nuevo_estado):
        """Cambia el estado del pedido si es una transición válida"""
        estados_validos = {
            'recibido': ['en_preparacion', 'cancelado'],
            'en_preparacion': ['listo', 'cancelado'],
            'listo': ['entregado', 'cancelado'],
            'entregado': ['pagado', 'cancelado'],
            'pagado': ['completado'],
            'completado': [],
            'cancelado': []
        }
        
        if nuevo_estado in estados_validos.get(self.estado, []):
            self.estado = nuevo_estado
            self.save(update_fields=['estado'])
            return True
        return False
    
    def puede_cancelarse(self):
        """Verifica si el pedido puede ser cancelado"""
        return self.estado not in ['pagado', 'completado', 'cancelado']
    
    def puede_modificarse(self):
        """Verifica si el pedido puede ser modificado"""
        return self.estado in ['recibido', 'en_preparacion']
