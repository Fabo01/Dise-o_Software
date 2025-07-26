# Backend/Infraestructura/Modelos/DeliveryApp_Modelo.py
from django.db import models
from django.db import models

class DeliveryAppModelo(models.Model):
    """
    Modelo para representar aplicaciones de delivery externas
    """
    nombre = models.CharField(max_length=100, unique=True)
    comision = models.DecimalField(max_digits=5, decimal_places=2)  # Porcentaje de comisión
    api_endpoint = models.URLField(blank=True, null=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    activa = models.BooleanField(default=True)
    configuracion_json = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'delivery_app'
        verbose_name = 'Aplicación de Delivery'
        verbose_name_plural = 'Aplicaciones de Delivery'
    
    def __str__(self):
        return f"{self.nombre} - {self.comision}% comisión"
    
    def calcular_comision(self, monto_pedido):
        """Calcula la comisión para un monto de pedido dado"""
        return monto_pedido * (self.comision / 100)
