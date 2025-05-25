from datetime import datetime
import bcrypt

from Backend.Dominio.Entidades.EntidadBase import EntidadBase


class UsuarioEntidad(EntidadBase):
    def __init__(self, username, password, mail, nombre, apellido, rol, telefono, fecha_registro, ultima_sesion):
        super().__init__()

        self._username = username
        self._password = None  # Se setea con set_password
        self.set_password(password)
        self._mail = mail
        self._nombre = nombre
        self._apellido = apellido
        self._rol = rol
        self._telefono = telefono
        self._fecha_registro = fecha_registro
        self._ultima_sesion = ultima_sesion

    def set_password(self, raw_password):
        """
        Hashea y almacena la contraseña.
        """
        if raw_password is None:
            raise ValueError("La contraseña no puede ser nula")
        if not isinstance(raw_password, bytes):
            raw_password = raw_password.encode('utf-8')
        self._password = bcrypt.hashpw(raw_password, bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        """
        Verifica si la contraseña ingresada coincide con el hash almacenado.
        """
        if not isinstance(raw_password, bytes):
            raw_password = raw_password.encode('utf-8')
        return bcrypt.checkpw(raw_password, self._password.encode('utf-8'))

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, valor):
        self._username = valor

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, valor):
        self.set_password(valor)

    @property
    def mail(self):
        return self._mail

    @mail.setter
    def mail(self, valor):
        self._mail = valor

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

