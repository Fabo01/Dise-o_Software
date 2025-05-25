from django.db import models

class ClienteModelo(models.Model):
    """
    Modelo ORM para la tabla Cliente
    """
    id = models.AutoField(unique=True, verbose_name='Id', primary_key=True)
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    telefono = models.CharField(max_length=15, null=True, blank=True, verbose_name="Teléfono")
    direccion = models.CharField(max_length=200, null=True, blank=True, verbose_name="Dirección")
    correo = models.EmailField(null=True, blank=True, verbose_name="Correo Electrónico")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    ultima_visita = models.DateTimeField(null=True, blank=True, verbose_name="Última Visita")
    estado = models.CharField(max_length=20, default="activo", verbose_name="Estado")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        db_table = "cliente"
        ordering = ["-fecha_registro"]

    def __str__(self):
        return f"{self.nombre} ({self.rut}) {self.fecha_registro}"