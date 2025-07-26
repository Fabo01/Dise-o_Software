# Backend/Infraestructura/Modelos/Transaccion_Modelo.py
from django.db import models
from decimal import Decimal

class TransaccionModelo(models.Model):
    """
    Modelo para representar transacciones de pago
    """
    ESTADOS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('exitosa', 'Exitosa'),
        ('fallida', 'Fallida'),
        ('cancelada', 'Cancelada'),
        ('reembolsada', 'Reembolsada'),
    ]
    
    pedido = models.ForeignKey(
        'Infraestructura.PedidoModelo',
        on_delete=models.CASCADE,
        related_name='transacciones'
    )
    medio_pago = models.ForeignKey(
        'Infraestructura.MedioPagoModelo',
        on_delete=models.PROTECT,
        related_name='transacciones'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    monto_comision = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='pendiente')
    codigo_referencia = models.CharField(max_length=100, unique=True)
    datos_adicionales = models.JSONField(default=dict, blank=True)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    fecha_procesamiento = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        db_table = 'transaccion'
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-fecha_transaccion']
    
    def __str__(self):
        return f"Transacción {self.codigo_referencia} - {self.get_estado_display()}"
    
    def es_exitosa(self):
        """Verifica si la transacción fue exitosa"""
        return self.estado == 'exitosa'
    
    def monto_neto(self):
        """Calcula el monto neto después de comisiones"""
        return self.monto - self.monto_comision
