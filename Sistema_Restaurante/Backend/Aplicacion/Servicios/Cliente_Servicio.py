from Backend.Dominio.objetos_valor.Correo_VO import CorreoVO
from Backend.Aplicacion.Servicios.Observer_Servicio import ObserverServicio
from Backend.Dominio.Factories.Cliente_Factory import ClienteFactory  # Importa la factory

class ClienteServicio:
    """
    Servicio que implementa los casos de uso relacionados con la gestión de clientes.
    """
    def __init__(self, cliente_repositorio, observer_service=None, cliente_factory=None):
        # Inyección de dependencias (Dependency Injection)
        self.cliente_repositorio = cliente_repositorio
        self.observer_service = observer_service or ObserverServicio()
        self.cliente_factory = cliente_factory or ClienteFactory()  # Usa la factory

    def registrar_cliente(self, datos_cliente):
        """
        Registra un nuevo cliente en el sistema
        
        Args:
            datos_cliente (dict): Datos del cliente a registrar, debe incluir nombre, correo y rut
            
        Returns:
            ClienteEntidad: La entidad cliente creada
            
        Raises:
            ValueError: Si ya existe un cliente con el mismo RUT o si faltan datos requeridos
        """
        # Validar datos requeridos
        if not datos_cliente.get('nombre'):
            raise ValueError("El nombre del cliente es obligatorio")
        if not datos_cliente.get('rut'):
            raise ValueError("El RUT del cliente es obligatorio")
        if not datos_cliente.get('correo'):
            raise ValueError("El correo del cliente es obligatorio")
        
        # Verificar si ya existe un cliente con ese RUT
        cliente_existente = self.cliente_repositorio.buscar_por_rut(datos_cliente['rut'])
        if cliente_existente:
            raise ValueError(f"Ya existe un cliente con el RUT: {datos_cliente['rut']}")
            
        # Crear objeto de valor correo
        try:
            correo = CorreoVO(datos_cliente['correo'])
        except ValueError as e:
            raise ValueError(str(e))
        
        # Crear entidad usando la factory
        cliente = self.cliente_factory.crear(
            nombre=datos_cliente['nombre'],
            correo=datos_cliente['correo'],
            rut=datos_cliente['rut'],
            telefono=datos_cliente.get('telefono', ''),
            direccion=datos_cliente.get('direccion', ''),
        )
        
        # Guardar usando el repositorio
        cliente_guardado = self.cliente_repositorio.guardar(cliente)
        # Notificar a los observadores si hay alguno registrado
        if self.observer_service:
            mensaje = f"Nuevo cliente registrado: {cliente_guardado.nombre} ({cliente_guardado.rut})"
            self.observer_service.notificar(mensaje)
        return cliente_guardado
        
    def actualizar_cliente(self, id, datos_cliente):
        """
        Actualiza los datos de un cliente existente
        
        Args:
            id (int): ID del cliente a actualizar
            datos_cliente (dict): Nuevos datos del cliente
            
        Returns:
            ClienteEntidad: La entidad cliente actualizada
            
        Raises:
            ValueError: Si no se encuentra el cliente o si los datos son inválidos
        """
        # Buscar el cliente
        cliente = self.cliente_repositorio.buscar_por_id(id)
        if not cliente:
            raise ValueError(f"No se encontró un cliente con ID: {id}")
            
        # Validar datos requeridos
        if not datos_cliente.get('nombre'):
            raise ValueError("El nombre del cliente es obligatorio")
        if not datos_cliente.get('correo'):
            raise ValueError("El correo del cliente es obligatorio")
            
        # Crear objeto de valor correo
        try:
            correo = CorreoVO(datos_cliente['correo'])
        except ValueError as e:
            raise ValueError(str(e))
            
        # Actualizar los datos
        cliente.actualizar_datos(
            nombre=datos_cliente['nombre'],
            correo=correo,
            telefono=datos_cliente.get('telefono'),
            direccion=datos_cliente.get('direccion'),
        )
        
        # Guardar los cambios
        return self.cliente_repositorio.guardar(cliente)
    
    def obtener_cliente(self, id):
        """
        Obtiene un cliente por su ID
        
        Args:
            id (int): ID del cliente a obtener
            
        Returns:
            ClienteEntidad: La entidad cliente o None si no se encuentra
        """
        return self.cliente_repositorio.buscar_por_id(id)
    
    def buscar_cliente_por_rut(self, rut):
        """
        Busca un cliente por su RUT
        
        Args:
            rut (str): RUT del cliente a buscar
            
        Returns:
            ClienteEntidad: La entidad cliente o None si no se encuentra
        """
        return self.cliente_repositorio.buscar_por_rut(rut)
    
    def buscar_clientes_por_nombre(self, nombre):
        """
        Busca clientes por coincidencia parcial en el nombre
        
        Args:
            nombre (str): Texto a buscar en los nombres
            
        Returns:
            List[ClienteEntidad]: Lista de clientes que coinciden con la búsqueda
        """
        return self.cliente_repositorio.buscar_por_nombre(nombre)
    
    def listar_clientes(self, solo_activos=False):
        """
        Lista todos los clientes o solo los activos
        
        Args:
            solo_activos (bool): Si True, solo muestra clientes activos
            
        Returns:
            List[ClienteEntidad]: Lista de clientes
        """
        if solo_activos:
            return self.cliente_repositorio.listar_activos()
        return self.cliente_repositorio.listar_todos()
    
    def desactivar_cliente(self, id):
        """
        Desactiva un cliente sin eliminarlo de la base de datos
        
        Args:
            id (int): ID del cliente a desactivar
            
        Returns:
            ClienteEntidad: La entidad cliente actualizada
            
        Raises:
            ValueError: Si no se encuentra el cliente
        """
        cliente = self.cliente_repositorio.buscar_por_id(id)
        if not cliente:
            raise ValueError(f"No se encontró un cliente con ID: {id}")
            
        cliente.desactivar()
        return self.cliente_repositorio.guardar(cliente)
    
    def activar_cliente(self, id):
        """
        Activa un cliente previamente desactivado
        
        Args:
            id (int): ID del cliente a activar
            
        Returns:
            ClienteEntidad: La entidad cliente actualizada
            
        Raises:
            ValueError: Si no se encuentra el cliente
        """
        cliente = self.cliente_repositorio.buscar_por_id(id)
        if not cliente:
            raise ValueError(f"No se encontró un cliente con ID: {id}")
            
        cliente.activar()
        return self.cliente_repositorio.guardar(cliente)
    
    def eliminar_cliente(self, id):
        """
        Elimina un cliente de la base de datos
        
        Args:
            id (int): ID del cliente a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        return self.cliente_repositorio.eliminar(id)
    
    def registrar_visita_cliente(self, id, fecha=None):
        """
        Registra una visita para un cliente
        
        Args:
            id (int): ID del cliente
            fecha (datetime, opcional): Fecha de la visita, si es None se usa la fecha actual
            
        Returns:
            ClienteEntidad: La entidad cliente actualizada
            
        Raises:
            ValueError: Si no se encuentra el cliente
        """
        cliente = self.cliente_repositorio.buscar_por_id(id)
        if not cliente:
            raise ValueError(f"No se encontró un cliente con ID: {id}")
            
        cliente.registrar_visita(fecha)
        return self.cliente_repositorio.guardar(cliente)