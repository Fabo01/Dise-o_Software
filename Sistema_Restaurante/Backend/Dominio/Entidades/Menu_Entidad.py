from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from .EntidadBase import EntidadBase
from ..Objetos_Valor.PrecioVO import PrecioVO
from ..Excepciones.DominioExcepcion import ValidacionExcepcion

class MenuEntidad(EntidadBase):
    """
    Entidad de dominio que representa un menú del restaurante.
    Contiene las reglas de negocio y validaciones para los menús.
    """
    
    def __init__(self, nombre: str, descripcion: str, precio: Decimal, 
                 categoria: str = "", tipo: str = "", imagen: str = "", 
                 tiempo_preparacion: int = 15):
        """
        Constructor de la entidad Menu.
        
        Args:
            nombre (str): Nombre del menú, no puede ser vacío
            descripcion (str): Descripción del menú
            precio (Decimal): Precio del menú, debe ser mayor a 0
            categoria (str, opcional): Categoría del menú (ej: entrada, plato principal, postre)
            tipo (str, opcional): Tipo de menú (ej: vegetariano, vegano, sin gluten)
            imagen (str, opcional): URL de la imagen del menú
            tiempo_preparacion (int, opcional): Tiempo de preparación en minutos
            
        Raises:
            ValidacionExcepcion: Si los datos proporcionados no son válidos
        """
        super().__init__()
        
        self._validar_datos_obligatorios(nombre, descripcion)
        
        self._nombre = nombre.strip()
        self._descripcion = descripcion.strip()
        self._categoria = categoria.strip()
        self._tipo = tipo.strip()
        self._imagen = imagen.strip()
        self._disponible = True
        self._ingredientes = []  # Lista de ingredientes necesarios
        self._veces_ordenado = 0  # Contador de popularidad
        
        # Validar y establecer tiempo de preparación
        if tiempo_preparacion <= 0:
            raise ValidacionExcepcion("El tiempo de preparación debe ser mayor a 0")
        self._tiempo_preparacion = tiempo_preparacion
        
        # Usar objeto de valor para el precio
        try:
            self._precio = PrecioVO(precio)
        except Exception as e:
            raise ValidacionExcepcion(f"Precio inválido: {str(e)}")
    
    def _validar_datos_obligatorios(self, nombre: str, descripcion: str):
        """Valida que los datos obligatorios estén presentes."""
        if not nombre or nombre.strip() == "":
            raise ValidacionExcepcion("El nombre del menú es obligatorio")
        
        if not descripcion or descripcion.strip() == "":
            raise ValidacionExcepcion("La descripción del menú es obligatoria")
        
        if len(nombre.strip()) < 2:
            raise ValidacionExcepcion("El nombre del menú debe tener al menos 2 caracteres")
        
        if len(nombre.strip()) > 200:
            raise ValidacionExcepcion("El nombre del menú no puede exceder 200 caracteres")
    
    # Getters
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def descripcion(self) -> str:
        return self._descripcion
    
    @property
    def precio(self) -> Decimal:
        return self._precio.valor
    
    @property
    def categoria(self) -> str:
        return self._categoria
    
    @property
    def tipo(self) -> str:
        return self._tipo
    
    @property
    def imagen(self) -> str:
        return self._imagen
    
    @property
    def disponible(self) -> bool:
        return self._disponible
    
    @property
    def ingredientes(self) -> List:
        return self._ingredientes.copy()
    
    @property
    def tiempo_preparacion(self) -> int:
        return self._tiempo_preparacion
    
    @property
    def veces_ordenado(self) -> int:
        return self._veces_ordenado
    
    # Métodos de negocio
    def actualizar_datos(self, nombre: str = None, descripcion: str = None, 
                        precio: Decimal = None, categoria: str = None, 
                        tipo: str = None, imagen: str = None, 
                        tiempo_preparacion: int = None):
        """
        Actualiza los datos del menú.
        
        Args:
            nombre (str, opcional): Nuevo nombre
            descripcion (str, opcional): Nueva descripción
            precio (Decimal, opcional): Nuevo precio
            categoria (str, opcional): Nueva categoría
            tipo (str, opcional): Nuevo tipo
            imagen (str, opcional): Nueva imagen
            tiempo_preparacion (int, opcional): Nuevo tiempo de preparación
            
        Raises:
            ValidacionExcepcion: Si los datos proporcionados no son válidos
        """
        if nombre is not None:
            if not nombre or nombre.strip() == "":
                raise ValidacionExcepcion("El nombre del menú es obligatorio")
            if len(nombre.strip()) < 2:
                raise ValidacionExcepcion("El nombre del menú debe tener al menos 2 caracteres")
            self._nombre = nombre.strip()
        
        if descripcion is not None:
            if not descripcion or descripcion.strip() == "":
                raise ValidacionExcepcion("La descripción del menú es obligatoria")
            self._descripcion = descripcion.strip()
        
        if precio is not None:
            try:
                self._precio = PrecioVO(precio)
            except Exception as e:
                raise ValidacionExcepcion(f"Precio inválido: {str(e)}")
        
        if categoria is not None:
            self._categoria = categoria.strip()
        
        if tipo is not None:
            self._tipo = tipo.strip()
        
        if imagen is not None:
            self._imagen = imagen.strip()
        
        if tiempo_preparacion is not None:
            if tiempo_preparacion <= 0:
                raise ValidacionExcepcion("El tiempo de preparación debe ser mayor a 0")
            self._tiempo_preparacion = tiempo_preparacion
        
        self.actualizar_fecha()
    
    def cambiar_disponibilidad(self, disponible: bool):
        """
        Cambia la disponibilidad del menú.
        
        Args:
            disponible (bool): Nueva disponibilidad del menú
        """
        self._disponible = disponible
        self.actualizar_fecha()
    
    def incrementar_contador_orden(self):
        """
        Incrementa el contador de veces ordenado.
        """
        self._veces_ordenado += 1
        self.actualizar_fecha()
    
    def agregar_ingrediente(self, ingrediente_id: str, cantidad: Decimal):
        """
        Agrega un ingrediente necesario para el menú.
        
        Args:
            ingrediente_id (str): ID del ingrediente
            cantidad (Decimal): Cantidad necesaria del ingrediente
            
        Raises:
            ValidacionExcepcion: Si los datos son inválidos
        """
        if not ingrediente_id:
            raise ValidacionExcepcion("El ID del ingrediente es obligatorio")
        
        if cantidad <= 0:
            raise ValidacionExcepcion("La cantidad debe ser mayor a 0")
        
        # Verificar si el ingrediente ya existe
        for ing in self._ingredientes:
            if ing['ingrediente_id'] == ingrediente_id:
                raise ValidacionExcepcion("El ingrediente ya está agregado al menú")
        
        self._ingredientes.append({
            'ingrediente_id': ingrediente_id,
            'cantidad': cantidad
        })
        self.actualizar_fecha()
    
    def remover_ingrediente(self, ingrediente_id: str):
        """
        Remueve un ingrediente del menú.
        
        Args:
            ingrediente_id (str): ID del ingrediente a remover
            
        Raises:
            ValidacionExcepcion: Si el ingrediente no existe
        """
        for i, ing in enumerate(self._ingredientes):
            if ing['ingrediente_id'] == ingrediente_id:
                self._ingredientes.pop(i)
                self.actualizar_fecha()
                return
        
        raise ValidacionExcepcion("El ingrediente no existe en el menú")
    
    def actualizar_cantidad_ingrediente(self, ingrediente_id: str, nueva_cantidad: Decimal):
        """
        Actualiza la cantidad de un ingrediente en el menú.
        
        Args:
            ingrediente_id (str): ID del ingrediente
            nueva_cantidad (Decimal): Nueva cantidad del ingrediente
            
        Raises:
            ValidacionExcepcion: Si el ingrediente no existe o la cantidad es inválida
        """
        if nueva_cantidad <= 0:
            raise ValidacionExcepcion("La cantidad debe ser mayor a 0")
        
        for ing in self._ingredientes:
            if ing['ingrediente_id'] == ingrediente_id:
                ing['cantidad'] = nueva_cantidad
                self.actualizar_fecha()
                return
        
        raise ValidacionExcepcion("El ingrediente no existe en el menú")
    
    def calcular_costo_ingredientes(self, precios_ingredientes: dict) -> Decimal:
        """
        Calcula el costo total de los ingredientes del menú.
        
        Args:
            precios_ingredientes (dict): Diccionario con precios por unidad de cada ingrediente
            
        Returns:
            Decimal: Costo total de los ingredientes
        """
        costo_total = Decimal('0.00')
        
        for ing in self._ingredientes:
            ingrediente_id = ing['ingrediente_id']
            cantidad = ing['cantidad']
            
            if ingrediente_id in precios_ingredientes:
                precio_unitario = precios_ingredientes[ingrediente_id]
                costo_total += cantidad * precio_unitario
        
        return costo_total
    
    def tiene_ingrediente(self, ingrediente_id: str) -> bool:
        """
        Verifica si el menú contiene un ingrediente específico.
        
        Args:
            ingrediente_id (str): ID del ingrediente a verificar
            
        Returns:
            bool: True si el menú contiene el ingrediente, False en caso contrario
        """
        return any(ing['ingrediente_id'] == ingrediente_id for ing in self._ingredientes)
    
    def es_valido_para_venta(self) -> bool:
        """
        Verifica si el menú está en condiciones de ser vendido.
        
        Returns:
            bool: True si el menú puede ser vendido, False en caso contrario
        """
        return (self._disponible and 
                self._nombre and 
                self._descripcion and 
                self._precio.valor > 0)
    
    def __str__(self) -> str:
        return f"Menu: {self._nombre} - ${self._precio.valor} ({'Disponible' if self._disponible else 'No disponible'})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, MenuEntidad):
            return False
        return self.id == other.id if self.id and other.id else self._nombre == other._nombre
    
    def __hash__(self) -> int:
        return hash(self.id) if self.id else hash(self._nombre)
