from django.db import models
from Backend.Dominio.Objetos_Valor.rut import Rut
from django.core.exceptions import ValidationError

class ClienteModelo(models.Model):
    """
    Modelo ORM para la tabla Cliente
    """
    rut = models.CharField(max_length=12, unique=True, primary_key=True, verbose_name="RUT", editable=False)
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

    def clean(self):
        if not Rut.validar(self.rut):
            raise ValidationError({"rut": "El RUT ingresado no es válido."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.rut}) {self.fecha_registro}"