from django.db import models
from .Pedido_Modelo import PedidoModelo
from .Menu_Modelo import MenuModelo
from .Ingrediente_Modelo import IngredienteModelo

class ItemPedidoModelo(models.Model):
    """
    Modelo ORM para la tabla ItemPedido
    """
    pedido = models.ForeignKey(PedidoModelo, on_delete=models.CASCADE, related_name="items", verbose_name="Pedido")
    menu = models.ForeignKey(MenuModelo, on_delete=models.PROTECT, verbose_name="Menú")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    notas = models.TextField(blank=True, verbose_name="Notas")
    personalizaciones = models.JSONField(null=True, blank=True, verbose_name="Personalizaciones")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Subtotal")
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Descuento")
    ingredientes = models.ManyToManyField(IngredienteModelo, blank=True, related_name="items_pedido", verbose_name="Ingredientes")

    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Items de Pedido"
        db_table = "item_pedido"

    def __str__(self):
        return f"Item {self.menu.nombre} x{self.cantidad} (Pedido #{self.pedido_id})"
