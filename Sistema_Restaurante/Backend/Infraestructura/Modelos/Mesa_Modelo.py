from django.db import models

class MesaModelo(models.Model):
    """
    Modelo ORM para la tabla Mesa
    """
    numero = models.CharField(max_length=10, unique=True, verbose_name="Número de Mesa")
    capacidad = models.PositiveIntegerField(verbose_name="Capacidad")
    ubicacion = models.CharField(max_length=100, blank=True, verbose_name="Ubicación")
    caracteristicas = models.CharField(max_length=200, blank=True, verbose_name="Características")
    estado = models.CharField(max_length=20, default="libre", verbose_name="Estado")
    cliente_actual = models.CharField(max_length=100, null=True, blank=True, verbose_name="Cliente Actual")
    hora_ocupacion = models.DateTimeField(null=True, blank=True, verbose_name="Hora de Ocupación")
    cantidad_personas = models.PositiveIntegerField(default=0, verbose_name="Cantidad de Personas")

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        db_table = "mesa"
        ordering = ["numero"]

    def __str__(self):
        return f"Mesa {self.numero} ({self.capacidad} personas) - {self.estado}"
