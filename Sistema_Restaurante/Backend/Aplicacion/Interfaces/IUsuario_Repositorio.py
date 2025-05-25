from abc import ABC, abstractmethod

class IUsuarioRepositorio(ABC):
    """
    Interfaz que define los métodos necesarios para un repositorio de usuarios.
    Sigue el patrón Repository para desacoplar la lógica de dominio del acceso a datos.
    """

    @abstractmethod
    def guardar(self, usuario):
        """
        Guarda o actualiza un usuario en el repositorio

        Args:
            usuario: La entidad usuario a guardar

        Returns:
            La entidad usuario actualizada
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id):
        """
        Busca un usuario por su ID

        Args:
            id: El ID del usuario a buscar

        Returns:
            La entidad usuario o None si no se encuentra
        """
        pass

    @abstractmethod
    def buscar_por_username(self, username):
        """
        Busca un usuario por su username

        Args:
            username: El username del usuario a buscar

        Returns:
            La entidad usuario o None si no se encuentra
        """
        pass

    @abstractmethod
    def listar_todos(self):
        """
        Lista todos los usuarios

        Returns:
            Lista de todas las entidades usuario
        """
        pass

    @abstractmethod
    def eliminar(self, id):
        """
        Elimina un usuario por su ID

        Args:
            id: El ID del usuario a eliminar

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        pass
