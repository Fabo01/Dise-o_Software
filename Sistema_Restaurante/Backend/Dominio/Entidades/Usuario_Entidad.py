from datetime import datetime
import bcrypt

from Backend.Dominio.Entidades.EntidadBase import EntidadBase
from Backend.Dominio.Objetos_Valor.Correo_VO import CorreoVO
from Backend.Dominio.Objetos_Valor.TelefonoVO import TelefonoVO
from Backend.Dominio.Objetos_Valor.RutVO import RutVO
from ..Excepciones.DominioExcepcion import ValidacionExcepcion


class UsuarioEntidad(EntidadBase):
    def __init__(self, rut, username, password, email, nombre, apellido, rol, telefono, fecha_registro, ultima_sesion, direccion=None):
        super().__init__()
        self._rut = RutVO(rut)  # RUT como objeto de valor, inmutable
        self._username = username
        self._password = None  # Se setea con el setter
        self.password = password  # Usar el setter para decidir si encriptar o no
        self._nombre = nombre
        self._apellido = apellido
        self._rol = rol
        self._fecha_registro = fecha_registro
        self._ultima_sesion = ultima_sesion
        self._direccion = direccion

        try:
            self._email = CorreoVO(email)
            self._telefono = TelefonoVO(telefono)
        except ValueError as e:
            raise ValidacionExcepcion(str(e))

    def set_password(self, raw_password):
        """
        Hashea y almacena la contraseña.
        """
        if raw_password is None:
            raise ValueError("La contraseña no puede ser nula")
        if not isinstance(raw_password, bytes):
            raw_password = raw_password.encode('utf-8')
        self._password = bcrypt.hashpw(raw_password, bcrypt.gensalt()).decode('utf-8')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, valor):
        # Si ya está encriptada (empieza con $2b$), no volver a encriptar
        if isinstance(valor, str) and valor.startswith("$2b$"):
            self._password = valor
        else:
            self.set_password(valor)

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, valor):
        self._username = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        self._email = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, valor):
        self._apellido = valor

    @property
    def rol(self):
        return self._rol

    @rol.setter
    def rol(self, valor):
        self._rol = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        self._telefono = valor

    @property
    def fecha_registro(self):
        return self._fecha_registro

    @fecha_registro.setter
    def fecha_registro(self, valor):
        self._fecha_registro = valor

    @property
    def ultima_sesion(self):
        return self._ultima_sesion

    @ultima_sesion.setter
    def ultima_sesion(self, valor):
        self._ultima_sesion = valor

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        self._direccion = valor

    @property
    def rut(self):
        return self._rut  # RUT es ahora un objeto de valor inmutable

    def actualizar_datos(self, nombre=None, apellido=None, email=None, telefono=None, rol=None, direccion=None):
        """
        Actualiza los datos del usuario de forma segura, similar a ClienteEntidad.
        """
        if nombre is not None:
            self._nombre = nombre
        if apellido is not None:
            self._apellido = apellido
        if email is not None:
            try:
                self._email = CorreoVO(email)
            except ValueError as e:
                raise ValidacionExcepcion(str(e))
        if telefono is not None:
            try:
                self._telefono = TelefonoVO(telefono)
            except ValueError as e:
                raise ValidacionExcepcion(str(e))
        if rol is not None:
            self._rol = rol
        if direccion is not None:
            self._direccion = direccion
        self.actualizar_fecha()

