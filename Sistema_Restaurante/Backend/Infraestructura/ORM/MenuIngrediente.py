from django.db import models
from django.core.validators import MinValueValidator
from .Ingrediente import Ingrediente
from .Menu import Menu

class MenuIngrediente(models.Model):
    """
    Modelo para representar la relación muchos a muchos entre Menú e Ingrediente,
    con información adicional sobre la cantidad requerida de cada ingrediente.
    """
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.FloatField(validators=[MinValueValidator(0.01)])
    
    class Meta:
        db_table = 'menu_ingrediente'
        unique_together = ('menu', 'ingrediente')
        
    def __str__(self):
        return f"{self.menu.nombre} - {self.ingrediente.nombre} ({self.cantidad} {self.ingrediente.unidad})"
    
    def es_preparable(self):
        """Verifica si hay suficiente cantidad del ingrediente para preparar el menú"""
        return self.ingrediente.cantidad >= self.cantidad
