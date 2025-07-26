from typing import List, Optional
from decimal import Decimal
from ..DTOs.MenuDTO import (
    MenuDTO, MenuCrearDTO, MenuActualizarDTO, MenuBusquedaDTO,
    MenuDisponibilidadDTO, MenuEstadisticasDTO, MenuListaDTO, 
    MenuDetalleDTO, MenuIngredienteDTO
)
from ...Dominio.Interfaces.IMenuRepositorio import IMenuRepositorio
from ...Dominio.Interfaces.IIngredienteRepositorio import IIngredienteRepositorio
from ...Dominio.Entidades.Menu_Entidad import MenuEntidad
from ...Dominio.Objetos_Valor.PrecioVO import PrecioVO
from ...Dominio.Excepciones.DominioExcepcion import ValidacionExcepcion
from ..Excepciones.AplicacionExcepcion import ServicioExcepcion, EntidadNoEncontradaExcepcion

class MenuServicio:
    """
    Servicio de aplicación para la gestión de menús.
    Implementa los casos de uso relacionados con los menús del restaurante.
    """
    
    def __init__(self, menu_repositorio: IMenuRepositorio, 
                 ingrediente_repositorio: IIngredienteRepositorio):
        """
        Constructor del servicio de menús.
        
        Args:
            menu_repositorio (IMenuRepositorio): Repositorio de menús
            ingrediente_repositorio (IIngredienteRepositorio): Repositorio de ingredientes
        """
        self._menu_repositorio = menu_repositorio
        self._ingrediente_repositorio = ingrediente_repositorio

    def crear_menu(self, menu_data: MenuCrearDTO) -> MenuDTO:
        """
        Caso de uso: Crear un nuevo menú.
        
        Args:
            menu_data (MenuCrearDTO): Datos del menú a crear
            
        Returns:
            MenuDTO: El menú creado
            
        Raises:
            ServicioExcepcion: Si ocurre un error durante la creación
        """
        try:
            # Verificar si ya existe un menú con el mismo nombre
            if self._menu_repositorio.existe_por_nombre(menu_data.nombre):
                raise ServicioExcepcion(f"Ya existe un menú con el nombre '{menu_data.nombre}'")
            
            # Crear la entidad del dominio
            menu_entidad = MenuEntidad(
                nombre=menu_data.nombre,
                descripcion=menu_data.descripcion,
                precio=menu_data.precio,
                categoria=menu_data.categoria,
                tipo=menu_data.tipo,
                imagen=menu_data.imagen,
                tiempo_preparacion=getattr(menu_data, 'tiempo_preparacion', 15)
            )
            
            # Guardar en el repositorio
            menu_guardado = self._menu_repositorio.guardar(menu_entidad)
            
            # Convertir a DTO y retornar
            return self._entidad_a_dto(menu_guardado)
            
        except ValidacionExcepcion as e:
            raise ServicioExcepcion(f"Error de validación: {str(e)}")
        except Exception as e:
            raise ServicioExcepcion(f"Error inesperado al crear el menú: {str(e)}")
    def obtener_menu_por_id(self, menu_id: int) -> Optional[MenuDTO]:
        """
        Caso de uso: Obtener un menú por su ID.
        
        Args:
            menu_id (int): ID del menú
            
        Returns:
            Optional[MenuDTO]: El menú encontrado o None
            
        Raises:
            ServicioExcepcion: Si ocurre un error durante la búsqueda
        """
        try:
            menu_entidad = self._menu_repositorio.obtener_por_id(menu_id)
            
            if menu_entidad is None:
                return None
            
            return self._entidad_a_dto(menu_entidad)
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener el menú: {str(e)}")
    
    def obtener_menu_por_nombre(self, nombre: str) -> Optional[MenuDTO]:
        """
        Caso de uso: Obtener un menú por su nombre.
        
        Args:
            nombre (str): Nombre del menú
            
        Returns:
            Optional[MenuDTO]: El menú encontrado o None
            
        Raises:
            ServicioExcepcion: Si ocurre un error durante la búsqueda
        """
        try:
            menu_entidad = self._menu_repositorio.obtener_por_nombre(nombre)
            
            if menu_entidad is None:
                return None
            
            return self._entidad_a_dto(menu_entidad)
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener el menú: {str(e)}")
    def actualizar_menu(self, menu_id: int, datos_actualizacion: MenuActualizarDTO) -> MenuDTO:
        """
        Caso de uso: Actualizar un menú existente.
        
        Args:
            menu_id (int): ID del menú a actualizar
            datos_actualizacion (MenuActualizarDTO): Datos de actualización
            
        Returns:
            MenuDTO: El menú actualizado
            
        Raises:
            EntidadNoEncontradaExcepcion: Si el menú no existe
            ServicioExcepcion: Si ocurre un error durante la actualización
        """
        try:
            # Obtener la entidad existente
            menu_entidad = self._menu_repositorio.obtener_por_id(menu_id)
            
            if menu_entidad is None:
                raise EntidadNoEncontradaExcepcion(f"No se encontró el menú con ID: {menu_id}")
            
            # Verificar duplicados de nombre si se está actualizando
            if (datos_actualizacion.nombre and 
                datos_actualizacion.nombre != menu_entidad.nombre and
                self._menu_repositorio.existe_por_nombre(datos_actualizacion.nombre)):
                raise ServicioExcepcion(f"Ya existe un menú con el nombre '{datos_actualizacion.nombre}'")
            
            # Actualizar la entidad
            menu_entidad.actualizar_datos(
                nombre=datos_actualizacion.nombre,
                descripcion=datos_actualizacion.descripcion,
                precio=datos_actualizacion.precio,
                categoria=datos_actualizacion.categoria,
                tipo=datos_actualizacion.tipo,
                imagen=datos_actualizacion.imagen,
                tiempo_preparacion=getattr(datos_actualizacion, 'tiempo_preparacion', None)
            )
            
            # Actualizar disponibilidad si es necesario
            if datos_actualizacion.disponible is not None:
                menu_entidad.cambiar_disponibilidad(datos_actualizacion.disponible)
            
            # Guardar cambios
            menu_actualizado = self._menu_repositorio.actualizar(menu_entidad)
            
            return self._entidad_a_dto(menu_actualizado)
            
        except (ValidacionExcepcion, EntidadNoEncontradaExcepcion) as e:
            raise e
        except Exception as e:
            raise ServicioExcepcion(f"Error inesperado al actualizar el menú: {str(e)}")
    def eliminar_menu(self, menu_id: int) -> bool:
        """
        Caso de uso: Eliminar un menú.
        
        Args:
            menu_id (int): ID del menú a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            EntidadNoEncontradaExcepcion: Si el menú no existe
            ServicioExcepcion: Si ocurre un error durante la eliminación
        """
        try:
            # Verificar que el menú existe
            if not self._menu_repositorio.existe(menu_id):
                raise EntidadNoEncontradaExcepcion(f"No se encontró el menú con ID: {menu_id}")
            
            # TODO: Verificar que el menú no esté siendo usado en pedidos activos
            
            # Eliminar el menú
            resultado = self._menu_repositorio.eliminar(menu_id)
            
            return resultado
            
        except EntidadNoEncontradaExcepcion as e:
            raise e
        except Exception as e:
            raise ServicioExcepcion(f"Error al eliminar el menú: {str(e)}")
    
    def listar_menus(self) -> List[MenuListaDTO]:
        """
        Caso de uso: Listar todos los menús.
        
        Returns:
            List[MenuListaDTO]: Lista de menús
            
        Raises:
            ServicioExcepcion: Si ocurre un error durante la consulta
        """
        try:
            menus_entidades = self._menu_repositorio.obtener_todos()
            
            return [self._entidad_a_lista_dto(menu) for menu in menus_entidades]
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al listar los menús: {str(e)}")
    
    def buscar_menus(self, criterios: MenuBusquedaDTO) -> List[MenuListaDTO]:
        """
        Caso de uso: Buscar menús según criterios específicos.
        
        Args:
            criterios (MenuBusquedaDTO): Criterios de búsqueda
            
        Returns:
            List[MenuListaDTO]: Lista de menús que cumplen los criterios
            
        Raises:
            ServicioExcepcion: Si ocurre un error durante la búsqueda
        """
        try:
            menus_encontrados = []
            
            # Búsqueda por texto
            if criterios.texto:
                menus_encontrados.extend(
                    self._menu_repositorio.buscar_por_texto(criterios.texto)
                )
            
            # Búsqueda por categoría
            if criterios.categoria:
                menus_categoria = self._menu_repositorio.obtener_por_categoria(criterios.categoria)
                if criterios.texto:
                    # Intersección de resultados
                    menus_encontrados = [m for m in menus_encontrados if m in menus_categoria]
                else:
                    menus_encontrados.extend(menus_categoria)
            
            # Si no hay criterios específicos, obtener todos
            if not criterios.texto and not criterios.categoria:
                menus_encontrados = self._menu_repositorio.obtener_todos()
            
            # Aplicar filtros adicionales
            menus_filtrados = self._aplicar_filtros_busqueda(menus_encontrados, criterios)
            
            return [self._entidad_a_lista_dto(menu) for menu in menus_filtrados]
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al buscar menús: {str(e)}")
    
    def obtener_menus_disponibles(self) -> List[MenuListaDTO]:
        """
        Caso de uso: Obtener solo los menús disponibles para venta.
        
        Returns:
            List[MenuListaDTO]: Lista de menús disponibles
            
        Raises:
            ServicioExcepcion: Si ocurre un error durante la consulta
        """
        try:
            menus_disponibles = self._menu_repositorio.obtener_disponibles()
            
            return [self._entidad_a_lista_dto(menu) for menu in menus_disponibles]
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener menús disponibles: {str(e)}")
    def verificar_disponibilidad_menu(self, menu_id: int) -> MenuDisponibilidadDTO:
        """
        Caso de uso: Verificar si un menú está disponible considerando ingredientes.
        
        Args:
            menu_id (int): ID del menú a verificar
            
        Returns:
            MenuDisponibilidadDTO: Estado de disponibilidad del menú
            
        Raises:
            EntidadNoEncontradaExcepcion: Si el menú no existe
            ServicioExcepcion: Si ocurre un error durante la verificación
        """
        try:
            menu_entidad = self._menu_repositorio.obtener_por_id(menu_id)
            
            if menu_entidad is None:
                raise EntidadNoEncontradaExcepcion(f"No se encontró el menú con ID: {menu_id}")
            
            disponibilidad = MenuDisponibilidadDTO(
                menu_id=menu_id,
                menu_nombre=menu_entidad.nombre,
                disponible=menu_entidad.disponible
            )
            
            # Si el menú está marcado como no disponible
            if not menu_entidad.disponible:
                disponibilidad.razon_no_disponible = "Menú marcado como no disponible"
                return disponibilidad
            
            # Verificar disponibilidad de ingredientes
            ingredientes_faltantes = []
            
            for ingrediente_menu in menu_entidad.ingredientes:
                ingrediente = self._ingrediente_repositorio.obtener_por_id(
                    ingrediente_menu['ingrediente_id']
                )
                
                if ingrediente is None:
                    ingredientes_faltantes.append(f"Ingrediente no encontrado: {ingrediente_menu['ingrediente_id']}")
                    continue
                
                cantidad_necesaria = ingrediente_menu['cantidad']
                if ingrediente.cantidad < cantidad_necesaria:
                    ingredientes_faltantes.append(f"{ingrediente.nombre} (necesita: {cantidad_necesaria}, disponible: {ingrediente.cantidad})")
            
            if ingredientes_faltantes:
                disponibilidad.disponible = False
                disponibilidad.razon_no_disponible = "Ingredientes insuficientes"
                disponibilidad.ingredientes_faltantes = ingredientes_faltantes
            
            return disponibilidad
            
        except EntidadNoEncontradaExcepcion as e:
            raise e
        except Exception as e:
            raise ServicioExcepcion(f"Error al verificar disponibilidad del menú: {str(e)}")
    
    def agregar_ingrediente_a_menu(self, menu_id: str, ingrediente_id: str, cantidad: Decimal) -> MenuDTO:
        """
        Caso de uso: Agregar un ingrediente a un menú.
        
        Args:
            menu_id (str): ID del menú
            ingrediente_id (str): ID del ingrediente
            cantidad (Decimal): Cantidad del ingrediente
            
        Returns:
            MenuDTO: El menú actualizado
            
        Raises:
            EntidadNoEncontradaExcepcion: Si el menú o ingrediente no existe
            ServicioExcepcion: Si ocurre un error durante la operación
        """
        try:
            # Verificar que el menú existe
            menu_entidad = self._menu_repositorio.obtener_por_id(menu_id)
            if menu_entidad is None:
                raise EntidadNoEncontradaExcepcion(f"No se encontró el menú con ID: {menu_id}")
            
            # Verificar que el ingrediente existe
            if not self._ingrediente_repositorio.existe(ingrediente_id):
                raise EntidadNoEncontradaExcepcion(f"No se encontró el ingrediente con ID: {ingrediente_id}")
            
            # Agregar el ingrediente al menú
            menu_entidad.agregar_ingrediente(ingrediente_id, cantidad)
            
            # Guardar cambios
            menu_actualizado = self._menu_repositorio.actualizar(menu_entidad)
            
            return self._entidad_a_dto(menu_actualizado)
            
        except (ValidacionExcepcion, EntidadNoEncontradaExcepcion) as e:
            raise e
        except Exception as e:
            raise ServicioExcepcion(f"Error al agregar ingrediente al menú: {str(e)}")
    
    def obtener_estadisticas_menus(self) -> MenuEstadisticasDTO:
        """
        Caso de uso: Obtener estadísticas generales de los menús.
        
        Returns:
            MenuEstadisticasDTO: Estadísticas de los menús
            
        Raises:
            ServicioExcepcion: Si ocurre un error durante el cálculo
        """
        try:
            todos_los_menus = self._menu_repositorio.obtener_todos()
            
            estadisticas = MenuEstadisticasDTO()
            estadisticas.total_menus = len(todos_los_menus)
            
            if estadisticas.total_menus == 0:
                return estadisticas
            
            # Contar disponibles y no disponibles
            estadisticas.menus_disponibles = sum(1 for m in todos_los_menus if m.disponible)
            estadisticas.menus_no_disponibles = estadisticas.total_menus - estadisticas.menus_disponibles
            
            # Estadísticas por categoría
            for menu in todos_los_menus:
                categoria = menu.categoria or "Sin categoría"
                estadisticas.por_categoria[categoria] = estadisticas.por_categoria.get(categoria, 0) + 1
            
            # Estadísticas por tipo
            for menu in todos_los_menus:
                tipo = menu.tipo or "Sin tipo"
                estadisticas.por_tipo[tipo] = estadisticas.por_tipo.get(tipo, 0) + 1
            
            # Estadísticas de precios
            precios = [menu.precio for menu in todos_los_menus]
            estadisticas.precio_minimo = min(precios)
            estadisticas.precio_maximo = max(precios)
            estadisticas.precio_promedio = sum(precios) / len(precios)
            
            return estadisticas
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al calcular estadísticas de menús: {str(e)}")
    
    def obtener_menus_por_categoria(self, categoria: str) -> List[MenuListaDTO]:
        """
        Caso de uso: Obtener menús por categoría.
        
        Args:
            categoria (str): Categoría de los menús
            
        Returns:
            List[MenuListaDTO]: Lista de menús de la categoría
            
        Raises:
            ServicioExcepcion: Si ocurre un error durante la consulta
        """
        try:
            menus_entidades = self._menu_repositorio.obtener_por_categoria(categoria)
            return [self._entidad_a_lista_dto(menu) for menu in menus_entidades]
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener menús por categoría: {str(e)}")

    def obtener_menus_por_tipo(self, tipo: str) -> List[MenuListaDTO]:
        """
        Caso de uso: Obtener menús por tipo.
        
        Args:
            tipo (str): Tipo de los menús
            
        Returns:
            List[MenuListaDTO]: Lista de menús del tipo
            
        Raises:
            ServicioExcepcion: Si ocurre un error durante la consulta
        """
        try:
            menus_entidades = self._menu_repositorio.buscar_por_tipo(tipo)
            return [self._entidad_a_lista_dto(menu) for menu in menus_entidades]
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener menús por tipo: {str(e)}")

    def obtener_menus_por_rango_precio(self, precio_min: Decimal, precio_max: Decimal) -> List[MenuListaDTO]:
        """
        Caso de uso: Obtener menús en un rango de precios.
        
        Args:
            precio_min (Decimal): Precio mínimo
            precio_max (Decimal): Precio máximo
            
        Returns:
            List[MenuListaDTO]: Lista de menús en el rango de precios
            
        Raises:
            ServicioExcepcion: Si ocurre un error durante la consulta
        """
        try:
            if precio_min > precio_max:
                raise ServicioExcepcion("El precio mínimo no puede ser mayor al precio máximo")
                
            menus_entidades = self._menu_repositorio.buscar_por_rango_precio(precio_min, precio_max)
            return [self._entidad_a_lista_dto(menu) for menu in menus_entidades]
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener menús por rango de precio: {str(e)}")

    def obtener_menus_por_popularidad(self, limite: int = 10) -> List[MenuListaDTO]:
        """
        Caso de uso: Obtener menús ordenados por popularidad.
        
        Args:
            limite (int): Número máximo de menús a retornar
            
        Returns:
            List[MenuListaDTO]: Lista de menús ordenados por popularidad
            
        Raises:
            ServicioExcepcion: Si ocurre un error durante la consulta
        """
        try:
            menus_entidades = self._menu_repositorio.listar_por_popularidad(limite)
            return [self._entidad_a_lista_dto(menu) for menu in menus_entidades]
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener menús por popularidad: {str(e)}")

    def obtener_menus_con_ingrediente(self, ingrediente_id: int) -> List[MenuListaDTO]:
        """
        Caso de uso: Obtener menús que contienen un ingrediente específico.
        
        Args:
            ingrediente_id (int): ID del ingrediente
            
        Returns:
            List[MenuListaDTO]: Lista de menús que contienen el ingrediente
            
        Raises:
            ServicioExcepcion: Si ocurre un error durante la consulta
        """
        try:
            menus_entidades = self._menu_repositorio.buscar_con_ingrediente(ingrediente_id)
            return [self._entidad_a_lista_dto(menu) for menu in menus_entidades]
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener menús con ingrediente: {str(e)}")

    def incrementar_contador_pedido(self, menu_id: int) -> bool:
        """
        Caso de uso: Incrementar el contador de veces ordenado de un menú.
        
        Args:
            menu_id (int): ID del menú
            
        Returns:
            bool: True si se actualizó correctamente
            
        Raises:
            EntidadNoEncontradaExcepcion: Si el menú no existe
            ServicioExcepcion: Si ocurre un error durante la actualización
        """
        try:
            menu_entidad = self._menu_repositorio.obtener_por_id(menu_id)
            
            if menu_entidad is None:
                raise EntidadNoEncontradaExcepcion(f"No se encontró el menú con ID: {menu_id}")
            
            # Incrementar contador en la entidad
            menu_entidad.incrementar_contador_orden()
            
            # Actualizar en el repositorio
            self._menu_repositorio.actualizar(menu_entidad)
            
            return True
            
        except EntidadNoEncontradaExcepcion as e:
            raise e
        except Exception as e:
            raise ServicioExcepcion(f"Error al incrementar contador de pedido: {str(e)}")

    def obtener_estadisticas_menus(self) -> MenuEstadisticasDTO:
        """
        Caso de uso: Obtener estadísticas generales de los menús.
        
        Returns:
            MenuEstadisticasDTO: Estadísticas de los menús
            
        Raises:
            ServicioExcepcion: Si ocurre un error durante el cálculo
        """
        try:
            todos_los_menus = self._menu_repositorio.obtener_todos()
            
            estadisticas = MenuEstadisticasDTO()
            estadisticas.total_menus = len(todos_los_menus)
            
            if estadisticas.total_menus == 0:
                return estadisticas
            
            # Contar disponibles y no disponibles
            estadisticas.menus_disponibles = sum(1 for m in todos_los_menus if m.disponible)
            estadisticas.menus_no_disponibles = estadisticas.total_menus - estadisticas.menus_disponibles
            
            # Estadísticas por categoría
            for menu in todos_los_menus:
                categoria = menu.categoria or "Sin categoría"
                estadisticas.por_categoria[categoria] = estadisticas.por_categoria.get(categoria, 0) + 1
            
            # Estadísticas por tipo
            for menu in todos_los_menus:
                tipo = menu.tipo or "Sin tipo"
                estadisticas.por_tipo[tipo] = estadisticas.por_tipo.get(tipo, 0) + 1
            
            # Estadísticas de precios
            precios = [menu.precio for menu in todos_los_menus]
            estadisticas.precio_minimo = min(precios)
            estadisticas.precio_maximo = max(precios)
            estadisticas.precio_promedio = sum(precios) / len(precios)
            
            return estadisticas
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al calcular estadísticas de menús: {str(e)}")
    
    # Métodos privados auxiliares
    def _entidad_a_dto(self, menu_entidad: MenuEntidad) -> MenuDTO:
        """Convierte una entidad Menu a MenuDTO."""
        return MenuDTO(
            id=menu_entidad.id,
            nombre=menu_entidad.nombre,
            descripcion=menu_entidad.descripcion,
            precio=menu_entidad.precio,
            categoria=menu_entidad.categoria,
            tipo=menu_entidad.tipo,
            imagen=menu_entidad.imagen,
            disponible=menu_entidad.disponible,
            tiempo_preparacion=menu_entidad.tiempo_preparacion,
            veces_ordenado=menu_entidad.veces_ordenado,
            fecha_creacion=menu_entidad.fecha_creacion,
            fecha_actualizacion=menu_entidad.fecha_actualizacion,
            ingredientes=menu_entidad.ingredientes
        )
    
    def _entidad_a_lista_dto(self, menu_entidad: MenuEntidad) -> MenuListaDTO:
        """Convierte una entidad Menu a MenuListaDTO."""
        return MenuListaDTO(
            id=menu_entidad.id,
            nombre=menu_entidad.nombre,
            precio=menu_entidad.precio,
            categoria=menu_entidad.categoria,
            disponible=menu_entidad.disponible,
            imagen=menu_entidad.imagen
        )
    
    def _aplicar_filtros_busqueda(self, menus: List[MenuEntidad], criterios: MenuBusquedaDTO) -> List[MenuEntidad]:
        """Aplica filtros adicionales a la lista de menús."""
        resultado = menus
        
        # Filtro por tipo
        if criterios.tipo:
            resultado = [m for m in resultado if m.tipo == criterios.tipo]
        
        # Filtro por disponibilidad
        if criterios.disponible is not None:
            resultado = [m for m in resultado if m.disponible == criterios.disponible]
        
        # Filtro por rango de precios
        if criterios.precio_min is not None:
            resultado = [m for m in resultado if m.precio >= criterios.precio_min]
        
        if criterios.precio_max is not None:
            resultado = [m for m in resultado if m.precio <= criterios.precio_max]
        
        # Filtro por ingrediente
        if criterios.con_ingrediente:
            resultado = [m for m in resultado if m.tiene_ingrediente(criterios.con_ingrediente)]
        
        return resultado
