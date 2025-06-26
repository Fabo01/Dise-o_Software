from Backend.Dominio.Entidades.Usuario_Entidad import UsuarioEntidad
from Backend.Dominio.Interfaces.IEntidad_Factory import IEntidadFactory
from datetime import datetime

class UsuarioFactory(IEntidadFactory):

    def construir_username(self, nombre, apellido, fecha_registro=None):
        """
        Construye el username con la primera letra del nombre, el apellido y el año.
        Ejemplo: Juan Pérez, 2025 -> jperez2025
        """
        inicial = nombre[0].lower() if nombre else ''
        apellido_limpio = apellido.replace(' ', '').lower() if apellido else ''
        if fecha_registro is None:
            fecha_registro = datetime.now()
        anio = fecha_registro.year
        return f"{inicial}{apellido_limpio}{anio}"

    def crear(self, nombre, apellido, password, email, rol, telefono, fecha_registro=None, ultima_sesion=None, direccion=None):
        nombre = nombre.strip().title() if nombre else ''
        apellido = apellido.strip().title() if apellido else ''
        username = self.construir_username(nombre, apellido, fecha_registro)
        if fecha_registro is None:
            fecha_registro = datetime.now()
        if ultima_sesion is None:
            ultima_sesion = datetime.now()
        return UsuarioEntidad(
            username=username,
            password=password,
            email=email,
            nombre=nombre,
            apellido=apellido,
            rol=rol,
            telefono=telefono,
            fecha_registro=fecha_registro,
            ultima_sesion=ultima_sesion,
            direccion=direccion
        )