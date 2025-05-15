from django.db import models

class IngredienteModelo(models.Model):
    '''
    Modelo ORM para la tabla Ingrediente
    '''
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad")
    categoria = models.CharField(max_length=50, verbose_name="Categoría")
    imagen = models.ImageField(upload_to='ingredientes/', null=True, blank=True, verbose_name="Imagen")
    unidad_medida = models.CharField(max_length=20, verbose_name="Unidad de Medida")
    fecha_vencimiento = models.DateField(verbose_name="Fecha de Vencimiento", null=True, blank=True)
    estado = models.CharField(max_length=20, default="activo", verbose_name="Estado")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    nivel_critico = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Nivel Crítico", null=True, blank=True)
    tipo = models.CharField(max_length=50, verbose_name="Tipo", null=True, blank=True)

    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"
        db_table = "ingrediente"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.cantidad} {self.unidad_medida})"

