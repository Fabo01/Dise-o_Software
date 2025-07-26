# Backend/Infraestructura/Modelos/MedioPago_Modelo.py
from django.db import models

class MedioPagoModelo(models.Model):
    """
    Modelo para representar medios de pago disponibles
    """
    TIPOS_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('tarjeta_debito', 'Tarjeta de Débito'),
        ('tarjeta_credito', 'Tarjeta de Crédito'),
        ('transferencia', 'Transferencia Bancaria'),
        ('app_pago', 'Aplicación de Pago'),
        ('crypto', 'Criptomoneda'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS_CHOICES)
    descripcion = models.TextField(blank=True)
    requiere_validacion = models.BooleanField(default=False)
    configuracion_api = models.JSONField(default=dict, blank=True)
    comision_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'medio_pago'
        verbose_name = 'Medio de Pago'
        verbose_name_plural = 'Medios de Pago'
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
    
    def calcular_comision(self, monto):
        """Calcula la comisión del medio de pago para un monto dado"""
        return monto * (self.comision_porcentaje / 100)
