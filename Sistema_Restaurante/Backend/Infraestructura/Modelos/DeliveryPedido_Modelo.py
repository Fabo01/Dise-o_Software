from django.db import models
from .Pedido_Modelo import PedidoModelo

class DeliveryPedidoModelo(models.Model):
    """
    Modelo ORM para la tabla DeliveryPedido
    """
    pedido = models.OneToOneField(PedidoModelo, on_delete=models.CASCADE, primary_key=True, related_name="delivery", verbose_name="Pedido Base")
    direccion_entrega = models.CharField(max_length=255, verbose_name="Dirección de Entrega")
    telefono_contacto = models.CharField(max_length=20, blank=True, verbose_name="Teléfono de Contacto")
    aplicacion_externa = models.CharField(max_length=50, null=True, blank=True, verbose_name="Aplicación Externa")
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Costo de Envío")
    repartidor = models.CharField(max_length=100, null=True, blank=True, verbose_name="Repartidor")
    codigo_seguimiento = models.CharField(max_length=100, null=True, blank=True, verbose_name="Código de Seguimiento")
    hora_salida = models.DateTimeField(null=True, blank=True, verbose_name="Hora de Salida")
    tiempo_estimado_entrega = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tiempo Estimado de Entrega (min)")

    class Meta:
        verbose_name = "Pedido Delivery"
        verbose_name_plural = "Pedidos Delivery"
        db_table = "delivery_pedido"

    def __str__(self):
        return f"Delivery #{self.pedido_id} - {self.direccion_entrega}"
