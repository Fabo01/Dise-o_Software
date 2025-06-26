from datetime import datetime
from Backend.Dominio.Entidades.Usuario_Entidad import UsuarioEntidad
from Backend.Dominio.Interfaces.IEntidad_Factory import IEntidadFactory
from Backend.Dominio.Objetos_Valor.rut import Rut
from Backend.Dominio.Objetos_Valor.TelefonoVO import TelefonoVO

class UsuarioFactory(IEntidadFactory):
    def crear(self, rut, username, nombre, apellido, rol, email, telefono, direccion, password, fecha_registro=None, ultima_sesion=None):
        if fecha_registro is None:
            from django.utils import timezone
            fecha_registro = timezone.now()
        if ultima_sesion is None:
            from django.utils import timezone
            ultima_sesion = timezone.now()
        # Convierte a VO si es string
        if isinstance(rut, str):
            rut = Rut(rut)
        if telefono and isinstance(telefono, str):
            telefono = TelefonoVO(telefono)
        return UsuarioEntidad(
            rut=rut,
            username=username,
            nombre=nombre,
            apellido=apellido,
            rol=rol,
            email=email,
            telefono=telefono,
            direccion=direccion,
            password=password,
            fecha_registro=fecha_registro,
            ultima_sesion=ultima_sesion
        )

class Rut:
    def __init__(self, valor):
        # Aquí puedes agregar validación real de RUT
        self.valor = valor

    @staticmethod
    def validar(valor):
        # Lógica de validación de RUT (opcional)
        return True  # O tu lógica real

    def __str__(self):
        return self.valor