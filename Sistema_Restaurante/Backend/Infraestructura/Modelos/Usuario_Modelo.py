from django.db import models
from django.utils import timezone

class UsuarioModelo(models.Model):
    """
    Modelo de Django para la tabla de usuarios.
    """
    id = models.AutoField(primary_key=True, unique=True, verbose_name='Id')
    username = models.CharField(max_length=150, unique=True, verbose_name='Username')
    password = models.CharField(max_length=128, verbose_name='Password', help_text='Contraseña encriptada')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    rol = models.CharField(max_length=100, null=True, verbose_name='Rol')
    email = models.EmailField(unique=True, verbose_name='Email')
    telefono = models.CharField(max_length=15, null=True, blank=True, verbose_name="Teléfono")
    direccion = models.CharField(max_length=100, verbose_name='Dirección', null=True)
    ultima_sesion = models.DateTimeField(default=timezone.now, verbose_name='Ultima Sesión')
    class Meta:
        db_table = 'usuarios'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["-ultima_sesion"]

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"