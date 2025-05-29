from django.db import models
from django.utils import timezone
from Backend.Dominio.Objetos_Valor.rut import Rut
from django.core.exceptions import ValidationError

class UsuarioModelo(models.Model):
    """
    Modelo de Django para la tabla de usuarios.
    """
    rut = models.CharField(max_length=12, unique=True, primary_key=True, verbose_name="RUT", editable=False)
    username = models.CharField(max_length=50, unique=True, verbose_name="Nombre de usuario")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, blank=True, verbose_name="Apellido")
    rol = models.CharField(max_length=20, verbose_name="Rol")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=15, null=True, blank=True, verbose_name="Teléfono")
    direccion = models.CharField(max_length=200, null=True, blank=True, verbose_name="Dirección")
    password = models.CharField(max_length=128, verbose_name="Contraseña")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    ultima_sesion = models.DateTimeField(null=True, blank=True, verbose_name="Última Sesión")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "usuarios"
        ordering = ["-fecha_registro"]

    def clean(self):
        if not Rut.validar(self.rut):
            raise ValidationError({"rut": "El RUT ingresado no es válido."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"