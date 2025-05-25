from django.db import models

class UsuarioModelo(models.Model):
    """
    Modelo de Django para la tabla de usuarios.
    """
    id = models.AutoField(primary_key=True, unique=True, verbose_name='Id')
    username = models.CharField(max_length=150, unique=True, verbose_name='Username')
    password = models.CharField(max_length=128, verbose_name='Password', help_text='Contraseña encriptada')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    rol = models.CharField(max_length=50, verbose_name='Rol')
    email = models.EmailField(unique=True, verbose_name='Email')
    telefono = models.CharField(max_length=15, null=True, blank=True, verbose_name='Teléfono')

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"