from django.db import models

class UsuarioModelo(models.Model):
    """
    Modelo de Django para la tabla de usuarios.
    """
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rol = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"