from django.db import models

class IngredienteModelo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad")
    unidad_medida = models.CharField(max_length=20, verbose_name="Unidad de Medida")
    fecha_vencimiento = models.DateField(verbose_name="Fecha de Vencimiento", null=True, blank=True)
    estado = models.CharField(max_length=20, default="activo", verbose_name="Estado")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    nivel_critico = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Nivel Crítico", null=True, blank=True)
    tipo = models.CharField(max_length=50, verbose_name="Tipo", null=True, blank=True)