from datetime import datetime
import bcrypt

from Backend.Dominio.Entidades.EntidadBase import EntidadBase
from Backend.Dominio.objetos_valor.Correo_VO import CorreoVO
from Backend.Dominio.objetos_valor.TelefonoVO import TelefonoVO
from ..Excepciones.DominioExcepcion import ValidacionExcepcion


class UsuarioEntidad(EntidadBase):
    def __init__(self, username, password, email, nombre, apellido, rol, telefono, fecha_registro, ultima_sesion, direccion=None):
        super().__init__()
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
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    def actualizar_datos(self, username, email, telefono=None, direccion=None):
        """
        Actualiza los datos del cliente
        
        Args:
            nombre (str): Nuevo nombre
            email (str): Nuevo correo
            telefono (str, opcional): Nuevo teléfono
            direccion (str, opcional): Nueva dirección
            
        Raises:
            ValidacionExcepcion: Si los datos proporcionados no son válidos
        """
        if not username:
            raise ValidacionExcepcion("El nombre es obligatorio")
        
        self._username = username
        
        try:
            # Permitir que 'email' sea str o CorreoVO
            if isinstance(email, CorreoVO):
                email_valor = email.valor
            else:
                email_valor = email
            self._email = CorreoVO(email_valor)
            
            if telefono is not None:
                self._telefono = TelefonoVO(telefono)
            
            if direccion is not None:
                self._direccion = direccion
                
            self.actualizar_fecha()
        except ValueError as e:
            raise ValidacionExcepcion(str(e))
    

