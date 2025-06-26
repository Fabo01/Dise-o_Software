from django.db import models

class MenuModelo(models.Model):
    """
    Modelo ORM para la tabla Menú
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    disponible = models.BooleanField(default=True, verbose_name="Disponible")
    tipo = models.CharField(max_length=50, blank=True, verbose_name="Tipo")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Menú"
        verbose_name_plural = "Menús"
        db_table = "menu"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
