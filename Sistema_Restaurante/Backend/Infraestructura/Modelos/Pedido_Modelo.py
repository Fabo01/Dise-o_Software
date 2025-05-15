from django.db import models
from .Cliente_Modelo import ClienteModelo
from .Mesa_Modelo import MesaModelo

class PedidoModelo(models.Model):
    """
    Modelo ORM para la tabla Pedido
    """
    cliente = models.ForeignKey(ClienteModelo, on_delete=models.PROTECT, related_name="pedidos", verbose_name="Cliente")
    mesa = models.ForeignKey(MesaModelo, on_delete=models.SET_NULL, null=True, blank=True, related_name="pedidos", verbose_name="Mesa")
    estado = models.CharField(max_length=20, default="recibido", verbose_name="Estado")
    fecha_pedido = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Pedido")
    hora_entrega = models.DateTimeField(null=True, blank=True, verbose_name="Hora de Entrega")
    notas = models.TextField(blank=True, verbose_name="Notas")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        db_table = "pedido"
        ordering = ["-fecha_pedido"]

    def __str__(self):
        return f"Pedido #{self.id} - {self.estado}"
